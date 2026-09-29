# Project status and how to resume

Where four-tone stands as of **2026-09-28**, what is decided, what is still open,
and the commands to pick the work back up.

## What exists

| Area | State |
| ---- | ----- |
| Firmware | Written, converted to PlatformIO, builds for the Arduino Nano (4828 bytes flash, 906 bytes RAM). Timing verified by simulation. **Never run on the real board.** |
| Driver board | Six fan driver rev A: schematic and layout done, ERC and DRC clean, fabrication files generated, ordered from JLCPCB on 2026-09-15, **arrived fully assembled by 2026-09-28**. Not yet powered or tested. |
| Head joint rev 02 | Printed in FDM and **working**: it voices with a 2" PVC pipe. |
| Head joint rev 03 | Hollowed for resin printing, 24% less material, quoted at $32.65 landed. **Modelled and exported only; never printed.** |
| Fan caddy | Printed and in use. |
| Pipes | Not cut. Target notes not chosen. |
| Enclosure | Built: an open-bottom wooden box. Dimensions and layout not documented. |
| Wooden head joint | **An exploration, not a decision.** Modelled and drawn to see whether it is viable to have made; see below. |

## Decided, and why

- **Channels follow the Nano's header order** (CH1 D3 to CH6 D11), so the gate
  traces fan out without crossing. The firmware drives pipes 1-4 on D3, D5, D6
  and D9.
- **Low-side AO3400A MOSFETs with an LED per channel**, fed from the supply's
  12 V rail, with the Nano powered from its 5 V rail. See
  [the board page](../hardware/pcb/README.md).
- **Print the head joints at JLC3DP in 9600 resin.** Rev 03 lands at $32.65
  against a US quote of over $200. See [print sourcing](print-sourcing.md).
- **The printed piece is called the head joint**, after the contrabass recorder
  head joint it follows.
- **Licensing is copyleft throughout**: GPL for firmware and tools, CERN-OHL-S
  for the board, CC-BY-SA for the mechanical design and documentation.

## Open, needing your input

1. **The four notes**, and the calibration measurement for cutting pipes: one
   test pipe's length and the frequency it plays. See [tuning](tuning.md).
2. **Print settings** for the FDM head joint and caddy (material, layer height,
   infill, orientation), for `mechanical/README.md`.
3. **Enclosure dimensions and layout**, for `mechanical/enclosure/`.
4. **Whether to pursue the wooden head joint at all.** It was explored to answer
   "is this viable to have made?", and the answer is yes: files exist to quote it
   from, but nothing has been built, and the printed part already works.

## Resume here: board bring-up

The boards have arrived, so the next session is testing them. Have ready:

- A multimeter, for the continuity and voltage checks.
- The power supply, wired to mains, with its 110/220 V switch set correctly, and
  leads to the board's screw terminal.
- The Arduino Nano and a USB cable.
- One fan, to test a single channel before fitting all four.
- PlatformIO Core, or the Arduino IDE, to upload the firmware. **PlatformIO is
  not installed on this machine yet** (`brew install platformio`).

The boards came fully assembled, so no soldering is needed. Start with the board
self test (`pio run -e selftest -t upload`), which walks all six channels one at
a time and narrates them over serial; see
[firmware/README.md](../firmware/README.md#testing-the-board). Upload the music
firmware afterwards.

## Next actions, in order

1. **Bring up the board**: follow [the build guide](build.md), which checks the
   supply, then the board with no Nano fitted, then the firmware, then one fan.
2. **Print one head joint rev 03** and compare how it voices against the working
   rev 02 before ordering four.
3. **Choose the notes, cut one test pipe, and calibrate** with
   `tools/pipe_length.py`.
4. **Fill in the TBDs**: pipe lengths, print settings, enclosure.
5. **Optional:** get the wooden version quoted from the package in
   [the wooden head joint guide](wood-head-joint.md).

## Rebuilding anything

All generated files can be recreated. Run these from the repository root.

| What | Command |
| ---- | ------- |
| Firmware build | `pio run` (or `pio run -e nano_old -t upload` for old-bootloader clones) |
| Board self test | `pio run -e selftest -t upload`, then `pio device monitor` |
| Schematic checks | `kicad-cli sch erc --severity-all hardware/pcb/four-tone-driver.kicad_sch` |
| Board checks | `kicad-cli pcb drc --schematic-parity --severity-all hardware/pcb/four-tone-driver.kicad_pcb` |
| Fabrication files | See `hardware/pcb/fabrication/rev-a/README.md` for the exact export settings |
| Head joint rev 03 | `freecadcmd -c "exec(open('tools/hollow_head_joint.py').read())"` |
| Wooden head joint model, STEP | `freecadcmd -c "exec(open('tools/model_wood_head_joint.py').read())"` |
| Wooden head joint DXF | `python3 tools/wood_dxf.py` (needs `ezdxf`) |
| Wooden head joint drawing | `python3 tools/draw_wood_head_joint.py docs/images/wood-head-joint.svg` |
| Licence check | `reuse lint` |

Dimensions for the wooden version live in `tools/wood_head_joint_spec.py`; the
model, drawing and DXF generators all read from it.

## Tools this work used

FreeCAD 1.1 (`freecadcmd`), KiCad 9.0.6 (`kicad-cli`), PlatformIO for the
firmware, and the Arduino IDE's bundled `arduino-cli` for a second opinion on
firmware builds. The FreeCAD models from January 2024 do not recompute cleanly in
1.1, so the scripts work from their saved geometry rather than rebuilding them;
see the version note in `mechanical/README.md`.
