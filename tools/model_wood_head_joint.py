# SPDX-FileCopyrightText: 2026 Matt Comeione
# SPDX-License-Identifier: GPL-3.0-or-later
"""Model the wooden head joint and export STEP files.

    freecadcmd -c "exec(open('tools/model_wood_head_joint.py').read())"

Builds the six pieces from tools/wood_head_joint_spec.py, checks them (no two
pieces occupy the same space, the windway gap is the intended size, the airway is
continuous), then writes mechanical/wood/wood-head-joint.FCStd, one STEP file per
piece, and an assembly STEP.

Dimensions are a concept carried over from the tested printed head joint; nothing
here has been built or voiced.
"""
import math
import os
import sys

import FreeCAD
import Part

sys.path.insert(0, os.path.abspath("tools"))
import wood_head_joint_spec as S

V = FreeCAD.Vector
OUTDIR = "mechanical/wood"
STEPDIR = os.path.join(OUTDIR, "step")
os.makedirs(STEPDIR, exist_ok=True)

half_out, half_in = S.OUT / 2, S.IN / 2


def box(x0, x1, y0, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


# ---- front board: window plus the labium bevel above it ---------------------
front = box(-half_out, -half_in, -half_out, half_out, 0, S.BOX_H)
window = box(-half_out, -half_in, -S.WIN_W / 2, S.WIN_W / 2, S.MOUTH, S.LABIUM)
# The bevel rises outward at LAB_ANGLE from the labium edge, which sits on the
# inside face. The window is therefore taller at the outer face.
rise = S.WALL * math.tan(math.radians(S.LAB_ANGLE))
bevel = Part.makePolygon([V(-half_in, -S.WIN_W / 2, S.LABIUM), V(-half_out, -S.WIN_W / 2, S.LABIUM + rise),
                          V(-half_out, -S.WIN_W / 2, S.LABIUM), V(-half_in, -S.WIN_W / 2, S.LABIUM)])
bevel = Part.Face(bevel).extrude(V(0, S.WIN_W, 0))
front = front.cut(window).cut(bevel)

# ---- back and side boards ---------------------------------------------------
back = box(half_in, half_out, -half_out, half_out, 0, S.BOX_H)
side_l = box(-half_in, half_in, -half_out, -half_in, 0, S.BOX_H)
side_r = box(-half_in, half_in, half_in, half_out, 0, S.BOX_H)

# ---- block: windway rabbet, wind chamber, inlet bore ------------------------
block = box(-half_in, half_in, -half_in, half_in, 0, S.BLOCK_H)
rabbet = box(-half_in, -half_in + S.WW_D, -S.WW_W / 2, S.WW_W / 2, S.BLOCK_H - S.WW_L, S.BLOCK_H)
chamber = box(-half_in, -half_in + S.CH_D, -S.CH_W / 2, S.CH_W / 2,
              S.BLOCK_H - S.WW_L - S.CH_H, S.BLOCK_H - S.WW_L)
bore = Part.makeCylinder(S.INLET / 2, S.BLOCK_H - S.WW_L - S.CH_H, V(0, 0, 0))
block = block.cut(rabbet).cut(chamber).cut(bore)

# ---- collar: glued on top, with the turned spigot ---------------------------
collar = box(-half_out, half_out, -half_out, half_out, S.BOX_H, S.BOX_H + S.COLLAR_H)
collar = collar.fuse(Part.makeCylinder(S.SPIGOT_D / 2, S.SPIGOT_L, V(0, 0, S.BOX_H + S.COLLAR_H)))
collar = collar.cut(Part.makeCylinder(S.COLLAR_BORE / 2, S.COLLAR_H + S.SPIGOT_L + 1, V(0, 0, S.BOX_H - 0.5)))
collar = collar.removeSplitter()

parts = [("front-board", front), ("back-board", back), ("side-board-left", side_l),
         ("side-board-right", side_r), ("block", block), ("collar", collar)]

# ---- checks -----------------------------------------------------------------
print("piece volumes (cm3):", {n: round(p.Volume / 1000, 1) for n, p in parts})
bad = []
for i in range(len(parts)):
    for j in range(i + 1, len(parts)):
        v = parts[i][1].common(parts[j][1]).Volume
        if v > 1e-6:
            bad.append((parts[i][0], parts[j][0], round(v, 3)))
print("overlapping pieces:", bad or "none")

assembly = parts[0][1]
for _, p in parts[1:]:
    assembly = assembly.fuse(p)
assembly = assembly.removeSplitter()
print(f"assembly: {len(assembly.Solids)} solid(s), {assembly.Volume / 1000:.1f} cm3, valid {assembly.isValid()}")
bb = assembly.BoundBox
print(f"envelope {bb.XLength:.1f} x {bb.YLength:.1f} x {bb.ZLength:.1f} mm "
      f"(box {S.BOX_H:g} + collar {S.COLLAR_H:g} + spigot {S.SPIGOT_L:g})")

# the windway itself: the void between the block's rabbet and the front board
probe = Part.makeBox(S.WW_D + 2, S.WW_W + 4, S.WW_L - 4,
                     V(-half_in - 1, -S.WW_W / 2 - 2, S.BLOCK_H - S.WW_L + 2))
ww = probe.cut(assembly_pieces := parts[0][1].fuse(parts[4][1]))
wb = ww.BoundBox
print(f"windway void: {wb.XLength:.2f} x {wb.YLength:.2f} mm cross-section "
      f"({'OK' if abs(wb.XLength - S.WW_D) < 1e-6 and abs(wb.YLength - S.WW_W) < 1e-6 else 'WRONG'})")

# the airway must run from the inlet, through the chamber and windway, to the mouth
air = Part.makeBox(120, 120, 200, V(-60, -60, -1)).cut(assembly)
inlet_pt = Part.Vertex(V(0, 0, 1))
mouth_pt = Part.Vertex(V(-half_in + S.WW_D / 2, 0, S.MOUTH + 0.5))
sol = [s for s in air.Solids if s.isInside(inlet_pt.Point, 1e-6, True)]
print("airway inlet to mouth is one connected void:",
      bool(sol) and sol[0].isInside(mouth_pt.Point, 1e-6, True))
spigot_clear = S.PIPE_ID - S.SPIGOT_D
print(f"spigot to PVC bore clearance: {spigot_clear:.2f} mm; spigot wall "
      f"{(S.SPIGOT_D - S.COLLAR_BORE) / 2:.2f} mm")

# ---- write ------------------------------------------------------------------
doc = FreeCAD.newDocument("wood-head-joint")
for name, shape in parts:
    o = doc.addObject("Part::Feature", name.replace("-", "_"))
    o.Shape = shape
    o.Label = name
    Part.export([o], os.path.join(STEPDIR, f"{name}.step"))
doc.recompute()
doc.saveAs(os.path.abspath(os.path.join(OUTDIR, "wood-head-joint.FCStd")))
Part.export(doc.Objects, os.path.join(STEPDIR, "wood-head-joint-assembly.step"))
print("wrote", OUTDIR, "with", len(parts) + 1, "STEP files")
