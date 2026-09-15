# Hardware

| Path | Contents |
| ---- | -------- |
| [`parts.md`](parts.md) | Everything to buy or make for the instrument |
| [`pcb/`](pcb/README.md) | The six fan driver: KiCad schematic and layout, BOM, circuit and layout notes |
| `pcb/fabrication/rev-a/` | Gerbers, drill files, BOM and CPL as ordered from JLCPCB |
| [`art/`](art/README.md) | Source artwork for the board's silkscreen logo |
| `datasheets/` | Reference datasheets (Arduino Nano pinout) |

## Editing the board

The KiCad project is `pcb/four-tone-driver.kicad_pro` and needs KiCad 9. It uses
only KiCad's standard symbol and footprint libraries, so it opens without extra
setup. `pcb/libraries/` is there for project-specific parts if any are added
later; reference them with `${KIPRJMOD}/libraries/...` so the project still opens
on other machines.

When the board changes, give it a new revision: update the revision on the
silkscreen and in the schematic title block, and generate a new
`pcb/fabrication/rev-<x>/` folder rather than overwriting `rev-a`, which records
what was actually made.

Per-user KiCad files (`*.kicad_prl`, `fp-info-cache`), backups and lock files are
git-ignored.
