# Mechanical

Each of the four voices is the same assembly: a 5015 blower fan, a printed fan
caddy, a printed head joint, and a length of 2" PVC pipe. All four head joints and
caddies are identical; the pipe length alone sets each pitch.

**Head joint** is the recorder term for the section that holds the windway, window
and labium. This design follows the head joint of a contrabass recorder, turned so
the air arrives from below: the fan caddy plugs into the bottom and the PVC pipe
into the top. On an organ, the same section is the mouth of a flue pipe, and the
pipe above it is the resonator.

```
 5015 blower ──> fan caddy ──> head joint (windway, labium) ──> 2" PVC pipe
                 hot glued      pipe length cut to pitch
```

## Parts

| Part      | Source                          | Notes |
| --------- | ------------------------------- | ----- |
| Head joint, rev 02 | `cad/fan_organ_pipe_rev_02.FCStd` | Windway, window and labium; the pipe plugs into its socket. Tested with 2" PVC. Solid block. |
| Head joint, rev 03 | `cad/fan_organ_pipe_rev_03.FCStd` | Rev 02 with the block hollowed (3 mm minimum walls), for resin and MJF printing. Not yet printed or tested. |
| Fan caddy | `cad/fan_mount_rev-01.FCStd`    | Holds the fan and ducts its outlet into the head joint's airway inlet. |
| Pipe      | 2" PVC, cut to length           | Same stock for all four voices; length sets pitch. See the [tuning guide](../docs/tuning.md). |
| Fan       | 5015 blower, 12 V (see [`../hardware/parts.md`](../hardware/parts.md)) | 50 x 50 x 15 mm, 19.5 mm outlet, 2-pin JST XH-style plug. |

### Head joint (`fan_organ_pipe_rev_02`)

Overall 67 x 67 x 150 mm. Dimensions below are read from the model's
sketch constraints; the roles are inferred from the constraint names.

| Parameter        | Value     | Role |
| ---------------- | --------- | ---- |
| `outerwall`      | 67.0 mm   | Outside diameter of the head joint |
| `innerwalld`     | 53.0 mm   | Bore, close to the 2" Sch 40 pipe inside diameter |
| `innerwalld` (wall009_1, wall010) | 61.0 mm | Socket the pipe slides into |
| `airwayinletd`   | 10.25 mm narrowing to 6.0 mm | Airway inlet from the caddy |
| `airwayrectx` x `airwayrecty` | 1.5 x 30.0 mm | Windway (flue) slot |
| `windowy`        | 32.03 mm  | Window / labium opening |

### Head joint rev 03 (`fan_organ_pipe_rev_03`)

Rev 02 with a cavity cut out of its solid block, to cut the material and weight of
resin and MJF prints. Everything from z 52 mm up (window, labium, bore and pipe
socket) and the outside shape are identical to rev 02, so it should voice the same;
that is untested.

| Feature | Value |
| ------- | ----- |
| Volume | 220.7 cm³, 24% less than rev 02's 289.7 cm³ |
| Minimum material | 3.0 mm everywhere between the cavity and any open space: outer wall, base, roof, and around the airway |
| Cavity roof | 45° cone, apex 3 mm below the top of the block, so FDM needs no support inside |
| Drain holes | 2 x 4 mm through the base at (15, ±10) mm, opposite the airway, so an SLA print does not trap resin. They can be plugged after printing. |

The cone roof is why the saving is 24% rather than most of the block's 174 cm³.
A flat roof at the same height would remove an estimated 1.5 to 1.8 times as much
material, but its underside cannot print without support trapped inside the
cavity.

The file is generated, not hand-modelled: `tools/hollow_head_joint.py` builds it
from rev 02 as saved and checks the wall thicknesses. It contains rev 02's solid
(`Rev02Solid`), the cavity (`Cavity`), and the result (`HeadJoint`, a Part Cut).
To change the wall thickness or drain holes, edit the script and run it with
FreeCAD's `freecadcmd`.

### Fan caddy (`fan_mount_rev-01`)

Overall 53 x 19.5 x 82 mm.

| Parameter        | Value     | Role |
| ---------------- | --------- | ---- |
| `fanwindowr`     | 18.0 mm radius | Intake window over the fan hub |
| `Diameter`       | 3.55 mm   | Fan screw hole |
| `innerw` x `innerh` | 17.5 x 12.5 mm | Duct at the fan outlet |
| `funnel002/003`  | 9.5 mm OD, 6.0 mm bore | Nozzle into the head joint's airway inlet |

## Printing

Print-ready STLs are in `stl/`, in millimetres, oriented as modelled (the head
joint stands on its caddy end, pipe socket up):

| File | Part | Volume | Size | Triangles |
| ---- | ---- | ------ | ---- | --------- |
| `stl/head-joint_rev-02.stl` | Head joint, solid | 289.5 cm³ | 67 x 67 x 150 mm | 4,660 |
| `stl/head-joint_rev-03.stl` | Head joint, hollowed | 220.6 cm³ | 67 x 67 x 150 mm | 10,206 |
| `stl/fan-caddy_rev-01.stl` | Fan caddy | 8.3 cm³ | 53 x 19.5 x 82 mm | 47,400 |

All were exported from the saved FreeCAD geometry without recomputing (see the
version note below), and checked as closed, manifold meshes with outward normals
and no self-intersections. Sampled against the CAD surfaces, the largest
deviation on outside and voicing surfaces is 0.040 mm on both head joints and
0.034 mm on the caddy. Rev 03's internal cavity cone deviates by up to about
0.12 mm; the facets sit inside the cavity, so they only make the walls thicker. The head joint
uses FreeCAD's standard mesher (0.05 mm linear, 0.20 rad angular deflection);
the caddy uses Netgen at its very fine setting, because the standard mesher left
small self-intersections in its funnel.

Print services such as JLC3DP quote directly from these files; select millimetres
when uploading. Head joint rev 02 is solid, so a resin or MJF print uses the full 289.5 cm³,
whereas an FDM print with partial infill uses less plastic. About 60% of that
volume (174 cm³) is the bottom 50 mm, which is solid apart from the airway, like a
recorder's block. Rev 03 hollows that section and is the one to order for resin or MJF: on JLC3DP it
lands at $32.65 against rev 02's $41.19. See the
[print sourcing guide](../docs/print-sourcing.md). For FDM either revision works;
infill already hollows rev 02.

Where to have them printed, what the options cost once tariffs and shipping are
counted, and the quotes gathered so far are in the
[print sourcing guide](../docs/print-sourcing.md).

To re-export after changing a model, select its `Body` in FreeCAD and use
**File > Export**, then check the mesh with **Meshes > Analyze > Evaluate and
repair mesh**.

Print material, layer height, infill, orientation and supports: TBD. Record the
settings that worked in `slicer/` as a slicer project, or here.

## A wooden version

The head joint can also be built in wood, the way a wooden organ pipe is: four
boards and a block glued into a square tube, with the windway formed as a gap
rather than a cut slot, plus a turned collar carrying the spigot for the PVC pipe.
The model is in `wood/` (FreeCAD, STEP and DXF), and the drawing and quote package
are in the [wooden head joint guide](../docs/wood-head-joint.md). It has not been
built or voiced.

## Assembly

The full build, including the electronics, is in the
[build guide](../docs/build.md).

1. Mount the fan in the caddy.
2. Seat the caddy nozzle in the head joint's airway inlet and secure it with hot
   glue. Hot glue is deliberate: it holds well enough and peels off, so a
   failed fan can be replaced.
3. Push the cut pipe into the head joint's socket.

## Enclosure

A custom-built wooden box with an open bottom holds the four voices and the
power supply. The driver board must sit within about 250 mm of each fan, because
the fan leads are 11" (280 mm) long.

Dimensions, internal layout and photos: TBD, to be recorded in `enclosure/`.

## Folders

| Folder       | Contents |
| ------------ | -------- |
| `cad/`       | FreeCAD source models. `cad/specifications/` is git-ignored: it holds the seller's fan drawings locally, which cannot be redistributed. |
| `stl/`       | Print-ready exports, named by part and revision. |
| `slicer/`    | Slicer project files (`.3mf`) with the settings that printed well. Empty so far. |
| `enclosure/` | Wooden box: dimensions, layout, photos. Empty so far. |
| `wood/`      | Wooden head joint: FreeCAD model, STEP files and DXF profiles, generated by `tools/`. |

Sliced G-code and FreeCAD backups (`.FCBak`, `.FCStd1`) are git-ignored.

## FreeCAD version note

Both models were saved in January 2024. Opening `fan_organ_pipe_rev_02` in
FreeCAD 1.1 logs "Reference constraint from this sketch cannot be used in
this expression" for several sketches (Sketch009 to 013, 018 to 020). The
saved geometry loads intact as one valid solid, but check those sketches'
expressions before recomputing and saving the model in 1.1.
