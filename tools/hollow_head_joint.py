# SPDX-FileCopyrightText: 2026 Matt Comeione
# SPDX-License-Identifier: GPL-3.0-or-later
"""Generate head joint rev 03: rev 02 with its solid block hollowed out.

Run from the repository root with FreeCAD's command-line interpreter:

    freecadcmd -c "exec(open('tools/hollow_head_joint.py').read())"

Rev 02's bottom section (z 0 to the windway exit) is solid apart from the airway
and holds about 60% of the part's volume. This removes a cavity from it while
keeping at least WALL of material everywhere:

- 3 mm outer wall, 3 mm base, and 3 mm of roof under the block's top face.
- At least 3 mm around the airway at every height. The keep-out is built from
  the airway's cross-section bounding boxes grown by WALL, which is never thinner
  than the true airway grown by WALL.
- A 45 degree conical roof, so an FDM print needs no support inside.
- Two drain holes through the base, so an SLA print does not trap liquid resin.

Rev 02 is used as saved (no recompute), because FreeCAD 1.1 cannot restore some
of its sketch expressions. Rev 03 is written as plain Part features.
"""
import math
import os

import FreeCAD
import Part

SRC = "mechanical/cad/fan_organ_pipe_rev_02.FCStd"
DST = "mechanical/cad/fan_organ_pipe_rev_03.FCStd"
WALL = 3.0              # minimum material thickness, mm
DRAIN_D = 4.0           # drain hole diameter, mm
DRAINS = [(15.0, 10.0), (15.0, -10.0)]   # drain hole centres (x, y), +X side, away from the airway
SLICE = 0.25            # keep-out slice height, mm
V = FreeCAD.Vector


def body_shape(path):
    doc = FreeCAD.openDocument(os.path.abspath(path))
    shape = [o for o in doc.Objects if o.TypeId == "PartDesign::Body"][0].Shape.copy()
    FreeCAD.closeDocument(doc.Name)
    return shape


base = body_shape(SRC)

# Outer radius and the top of the solid block: the highest z where a section is
# still the full outer circle plus the airway.
R = max(abs(v) for v in (base.BoundBox.YMin, base.BoundBox.YMax))
z, block_top = 0.0, None
while z < base.BoundBox.ZMax:
    wires = base.slice(V(0, 0, 1), z + 1e-3)
    outer = [w for w in wires if abs(w.BoundBox.XLength - 2 * R) < 0.01 and abs(w.BoundBox.YLength - 2 * R) < 0.01]
    if len(wires) != 2 or len(outer) != 1:
        block_top = z
        break
    z += 0.05
# step back to the last solid section
block_top = round(block_top - 0.05, 2)

# Airway void inside the block
envelope = Part.makeCylinder(R, block_top, V(0, 0, 0))
airway = envelope.cut(base.common(envelope))
airway = Part.makeCompound([s for s in airway.Solids if s.Volume > 1.0])

# Keep-out around the airway: per-slice bounding boxes grown by WALL
boxes = []
z = 0.0
while z < block_top:
    z1 = min(z + SLICE, block_top)
    xs0 = ys0 = math.inf
    xs1 = ys1 = -math.inf
    for zz in (z + 1e-3, (z + z1) / 2, z1 - 1e-3):
        for w in airway.slice(V(0, 0, 1), zz):
            bb = w.BoundBox
            xs0, xs1 = min(xs0, bb.XMin), max(xs1, bb.XMax)
            ys0, ys1 = min(ys0, bb.YMin), max(ys1, bb.YMax)
    if xs0 < math.inf:
        boxes.append(Part.makeBox(xs1 - xs0 + 2 * WALL, ys1 - ys0 + 2 * WALL, z1 - z + 2 * WALL,
                                  V(xs0 - WALL, ys0 - WALL, z - WALL)))
    z = z1
keepout = boxes[0].multiFuse(boxes[1:]).removeSplitter()

# Cavity: cylinder, then a 45 degree cone whose apex sits WALL below the block top
rc = R - WALL
apex = block_top - WALL
cone_start = apex - rc
cavity = Part.makeCylinder(rc, cone_start - WALL, V(0, 0, WALL)).fuse(
    Part.makeCone(rc, 0, rc, V(0, 0, cone_start)))
cavity = cavity.cut(keepout).removeSplitter()

drains = Part.makeCompound([Part.makeCylinder(DRAIN_D / 2, WALL + 1.0, V(x, y, -0.5)) for x, y in DRAINS])
result = base.cut(cavity.fuse(drains)).removeSplitter()

# ---- verification -------------------------------------------------------
exterior = Part.makeCylinder(R + 10, block_top + 10, V(0, 0, -10)).cut(Part.makeCylinder(R, block_top + 10, V(0, 0, 0)))
above = Part.makeCylinder(R, 10, V(0, 0, block_top))
checks = {
    "cavity to airway": cavity.distToShape(airway)[0],
    "cavity to outside wall and base": cavity.distToShape(exterior)[0],
    "cavity to block top": cavity.distToShape(above)[0],
    "drain holes to airway": drains.distToShape(airway)[0],
}
print(f"outer radius {R:.2f} mm, block top z {block_top:.2f} mm, cone from z {cone_start:.2f} to {apex:.2f}")
print(f"airway void {airway.Volume / 1000:.2f} cm3, cavity {cavity.Volume / 1000:.2f} cm3")
for name, dist in checks.items():
    print(f"  {name}: {dist:.3f} mm {'OK' if dist >= WALL - 1e-3 else 'TOO THIN'}")
drains_open = all(Part.makeCylinder(DRAIN_D / 2, 1.0, V(x, y, WALL)).common(cavity).Volume > 0 for x, y in DRAINS)
print(f"  drain holes open into the cavity: {drains_open}")
print(f"rev 02 {base.Volume / 1000:.2f} cm3 -> rev 03 {result.Volume / 1000:.2f} cm3 "
      f"({(1 - result.Volume / base.Volume) * 100:.1f}% less), solids {len(result.Solids)}, valid {result.isValid()}")
assert all(d >= WALL - 1e-3 for d in checks.values()) and drains_open and result.isValid() and len(result.Solids) == 1

# ---- write rev 03 --------------------------------------------------------
doc = FreeCAD.newDocument("fan_organ_pipe_rev_03")
src = doc.addObject("Part::Feature", "Rev02Solid"); src.Shape = base
src.Label = "Head joint rev 02 (as saved)"
cav = doc.addObject("Part::Feature", "Cavity"); cav.Shape = cavity.fuse(drains).removeSplitter()
cav.Label = f"Cavity and drain holes ({WALL:g} mm walls)"
cut = doc.addObject("Part::Cut", "HeadJoint"); cut.Base = src; cut.Tool = cav
cut.Label = "Head joint rev 03"
doc.recompute()
assert cut.Shape.isValid() and abs(cut.Shape.Volume - result.Volume) < 1.0
doc.saveAs(os.path.abspath(DST))
print(f"saved {DST}: HeadJoint {cut.Shape.Volume / 1000:.2f} cm3")
