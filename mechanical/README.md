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
| Head joint | `cad/fan_organ_pipe_rev_02.FCStd` | Windway, window and labium; the pipe plugs into its socket. Tested with 2" PVC. |
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
| `stl/head-joint_rev-02.stl` | Head joint | 289.5 cm³ | 67 x 67 x 150 mm | 4,660 |
| `stl/fan-caddy_rev-01.stl` | Fan caddy | 8.3 cm³ | 53 x 19.5 x 82 mm | 47,400 |

Both were exported from the saved FreeCAD geometry without recomputing (see the
version note below), and checked as closed, manifold meshes with outward normals
and no self-intersections. Sampled against the CAD surfaces, the largest
deviation is 0.040 mm on the head joint and 0.034 mm on the caddy. The head joint
uses FreeCAD's standard mesher (0.05 mm linear, 0.20 rad angular deflection);
the caddy uses Netgen at its very fine setting, because the standard mesher left
small self-intersections in its funnel.

Print services such as JLC3DP quote directly from these files; select millimetres
when uploading. The head joint is solid, so a resin or MJF print uses the full
289.5 cm³, whereas an FDM print with partial infill uses less plastic. About 60%
of that volume (174 cm³) is the bottom 50 mm, which is solid apart from the
airway, like a recorder's block. Hollowing that section, while keeping walls
around the airway, is the most effective way to cut the cost of a resin or MJF
print.

JLC3DP instant quotes for the head joint, 2026-09-15, per unit before shipping:

| Material | Price |
| -------- | ----- |
| 9600 resin (SLA, matte white) | $26.35 |
| Imagine Black resin (SLA) | $78.20 |

Prices change; re-quote from the STL before ordering.

To re-export after changing a model, select its `Body` in FreeCAD and use
**File > Export**, then check the mesh with **Meshes > Analyze > Evaluate and
repair mesh**.

Print material, layer height, infill, orientation and supports: TBD. Record the
settings that worked in `slicer/` as a slicer project, or here.

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

Sliced G-code and FreeCAD backups (`.FCBak`, `.FCStd1`) are git-ignored.

## FreeCAD version note

Both models were saved in January 2024. Opening `fan_organ_pipe_rev_02` in
FreeCAD 1.1 logs "Reference constraint from this sketch cannot be used in
this expression" for several sketches (Sketch009 to 013, 018 to 020). The
saved geometry loads intact as one valid solid, but check those sketches'
expressions before recomputing and saving the model in 1.1.
