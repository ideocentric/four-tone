# License

four-tone is open source under copyleft licenses. Each part of the project
uses the license suited to its kind of work, and each requires that modified
versions be shared under the same terms.

| Part | Paths | License |
| ---- | ----- | ------- |
| Firmware and tools | `firmware/`, `platformio.ini`, `tools/` | [GNU GPL v3.0 or later](LICENSES/GPL-3.0-or-later.txt) |
| Hardware | `hardware/` (PCB design, parts list), `docs/images/six-fan-driver-rev-a-schematic.pdf` | [CERN Open Hardware Licence v2, Strongly Reciprocal](LICENSES/CERN-OHL-S-2.0.txt) |
| Design | `mechanical/` (3D models), `docs/`, and everything else not listed above | [Creative Commons Attribution-ShareAlike 4.0](LICENSES/CC-BY-SA-4.0.txt) |

Documentation inside a part's folder (for example `firmware/README.md`)
follows that part's license.

Copyright 2024-2026 Matt Comeione.

The per-file mapping is recorded in [`REUSE.toml`](REUSE.toml), following the
[REUSE](https://reuse.software) specification. Where a source file carries its
own `SPDX-License-Identifier` header, that header applies.

## Third-party material

| File | Copyright | License |
| ---- | --------- | ------- |
| `hardware/datasheets/Pinout-NANO_latest.pdf` | Arduino SA | CC BY-SA 4.0 |

The firmware builds against the Arduino core, which is licensed separately
under the GNU LGPL v2.1.

## Hardware source location

CERN-OHL-S asks that products made from the design carry a notice pointing to
where the source can be found. The source location is:

<https://github.com/ideocentric/four-tone>

The driver board carries it on its silkscreen, next to the licence name, and
the schematic carries it in the title block.