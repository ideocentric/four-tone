# Hardware

## `pcb/`

KiCad project for the board the Arduino plugs into, which switches the four
12 V fans. Keep the KiCad project files (`.kicad_pro`, `.kicad_sch`,
`.kicad_pcb`) directly in `pcb/`.

- `libraries/symbols/`, `libraries/footprints/`, `libraries/3dmodels/`:
  anything not in the stock KiCad libraries. Reference them from the project
  library tables with `${KIPRJMOD}/libraries/...` so the project opens on any
  machine.
- `fabrication/<rev>/`: outputs actually sent to a fab house (Gerbers, drill,
  BOM, pick-and-place), e.g. `fabrication/rev-a/`. Scratch exports in `pcb/`
  itself are git-ignored.

`*.kicad_prl` (per-user view state), backups and lock files are git-ignored.

## `datasheets/`

Datasheets for the parts the board design depends on.
