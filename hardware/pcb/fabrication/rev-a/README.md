# Six fan driver, rev A: JLCPCB fabrication files

Generated 2026-09-15 with `kicad-cli` (KiCad 9.0.6) from
`../../four-tone-driver.kicad_pcb` at commit `da0a9be`. Regenerate these
whenever the board or schematic changes; they are outputs, not sources.

| File | Upload to JLCPCB as |
| ---- | ------------------- |
| `six-fan-driver-rev-a-gerbers.zip` | Gerber file (PCB order) |
| `six-fan-driver-rev-a-bom.csv` | BOM (PCB Assembly) |
| `six-fan-driver-rev-a-cpl.csv` | CPL / pick-and-place (PCB Assembly) |
| `gerbers/` | The zip's contents, unzipped for review and diffs |

## Board

- 130 x 70 mm, 2 layers, 1.6 mm FR-4 (JLCPCB defaults are fine).
- Minimums used: 0.2 mm track and clearance, 0.6 mm via with 0.3 mm drill.
- Holes: 107 plated (61 x 0.3 mm vias, 42 x 1.0 mm, 4 x 1.3 mm) and
  4 x 3.2 mm non-plated mounting holes, matching the board file.
- DRC before export: 0 violations, 0 unconnected, 0 schematic parity issues.

## Gerber and drill settings

These follow JLCPCB's KiCad guide.

- Layers: F.Cu, B.Cu, F.Paste, B.Paste, F.SilkS, B.SilkS, F.Mask, B.Mask,
  Edge.Cuts. The back paste and silkscreen layers are empty; all parts are on
  the top side.
- Protel filename extensions, no X2 attributes, no netlist attributes, soldermask
  subtracted from silkscreen, 4.6 coordinate precision in mm, no Gerber job file.
- Drill: Excellon, mm, decimal, absolute origin, alternate oval mode, separate
  PTH and NPTH files, Gerber X2 drill maps.

## BOM and CPL

- 12 BOM lines, 50 placed parts, all top side, every line with an LCSC number.
  Mounting holes and the reference-only Nano symbol (A1) are not placed.
- The CPL uses the same absolute origin as the Gerbers.
- Rotation corrections from the
  [JLCKicadTools](https://github.com/matthewlai/JLCKicadTools) rotation table
  (`cpl_rotations_db.csv`, last updated 2024-09-11) were applied:
  - `SOT-23` -90 degrees: Q1-Q6
  - `CP_Elec_6.3x7.7` +180 degrees: C1

  No correction was listed for the other footprints, so they keep KiCad's
  rotation.

## Check in JLCPCB's placement preview before paying

The rotation table is community data, not JLCPCB's, so treat the preview as the
final authority:

- **Q1-Q6** (AO3400A): gate and source pads on the side away from the fan
  connectors, drain toward them.
- **D1-D6** (SS14): cathode band toward the left (+12 V side of each channel).
- **D11-D16** (LEDs): cathode toward the left, the switched-return side.
- **C1** (100 uF): positive terminal on the left, toward the power terminal.
- **Through-hole parts** (J1, J2, J3, J11-J16): KiCad places these by pin 1,
  not the body centre, so their preview position may look offset. Either let
  JLCPCB adjust them, or leave them off the assembly order and solder them by
  hand. They are all Extended parts.
