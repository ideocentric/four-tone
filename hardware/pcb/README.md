# Six fan driver, rev A

![Six fan driver rev A, top view](../../docs/images/six-fan-driver-rev-a-top.png)

An Arduino Nano carrier board with six low-side MOSFET fan channels. four-tone
uses four of them; the other two are spare for other projects. It is designed for
JLCPCB fabrication and assembly, and rev A was ordered on 2026-09-15.

| File | What it is |
| ---- | ---------- |
| `four-tone-driver.kicad_sch` | Schematic (KiCad 9). [PDF](../../docs/images/six-fan-driver-rev-a-schematic.pdf) |
| `four-tone-driver.kicad_pcb` | Board layout (KiCad 9) |
| `four-tone-driver.kicad_pro` | Project settings, including the `Power` net class |
| `fabrication/rev-a/` | Gerbers, drill files, BOM and CPL as ordered, with the export settings |

The KiCad files keep the project's original `four-tone-driver` name; the board
itself is titled "six fan driver". Every symbol carries its JLCPCB/LCSC part
number in an `LCSC` field.

## BOM

| Designators | Qty | Part | Package | LCSC | JLC type |
| ----------- | --- | ---- | ------- | ---- | -------- |
| Q1-Q6 | 6 | AO3400A N-MOSFET, 30 V 5.7 A | SOT-23 | C20917 | Basic |
| D1-D6 | 6 | SS14 Schottky flyback diode, 1 A 40 V | SMA | C2480 | Basic |
| D11-D16 | 6 | Red LED, channel indicator | 0603 | C2286 | Basic |
| R1-R6 | 6 | 1 k gate resistor | 0603 | C21190 | Basic |
| R11-R16 | 6 | 100 k gate pull-down | 0603 | C25803 | Basic |
| R21-R26 | 6 | 4.7 k LED resistor | 0603 | C23162 | Basic |
| C1 | 1 | 100 uF 25 V electrolytic, 12 V bulk | SMD 6.3 x 7.7 mm | C72477 | Extended |
| C2, C4 | 2 | 10 uF 25 V X5R, 12 V and 5 V bulk | 0805 | C15850 | Basic |
| C3, C5 | 2 | 100 nF 50 V X7R, 12 V and 5 V decoupling | 0603 | C14663 | Basic |
| J1 | 1 | 4-pin screw terminal, 5.08 mm | THT | C2915641 | Extended |
| J2, J3 | 2 | 1x15 female header, 2.54 mm (Nano socket) | THT | C7499333 | Extended |
| J11-J16 | 6 | JST B2B-XH-A, 2-pin vertical (genuine JST) | THT | C158012 | Extended |

Availability was checked on 2026-09-15 through tscircuit's jlcsearch mirror of
the JLCPCB catalogue, and every line was in stock. Stock changes, so re-check in
JLCPCB's BOM tool when ordering.

## Circuit

- **Power, J1:** pin 1 +12 V, pin 2 GND, pin 3 +5 V, pin 4 GND. The two grounds
  are joined on the board, so the supply's 5 V and 12 V returns must be common.
  Confirm this with a meter before connecting (see the
  [build guide](../../docs/build.md)).
- **Logic power:** +5 V feeds the Nano's `+5V` pin directly through the socket,
  bypassing its regulator. `VIN` is not connected. The Nano reference design has
  a Schottky diode on USB VBUS, so the supply cannot back-feed a computer while
  USB is plugged in for programming. Clones vary; check the ones you use.
- **Each fan channel:** a Nano PWM pin drives the AO3400A gate through 1 k, with
  a 100 k pull-down to GND so the fan stays off while the Nano resets or is
  unplugged. The MOSFET switches the fan's return (connector pin 2) to GND. An
  SS14 across the fan clamps the lead inductance. A red LED with 4.7 k from
  +12 V to the switched return lights when the channel is on (about 2 mA) and
  follows the PWM ramp. It lights with no fan plugged in, which helps testing.
- **Fan connectors J11-J16:** pin 1 +12 V (marked + on the silkscreen), pin 2
  switched return.
- **Current:** the fans are rated 0.18 A. The design allows 0.5 A per channel for
  start-up and 3 A for all six. The AO3400A is about 30 mOhm at 5 V gate drive,
  so it dissipates under 10 mW per channel.

## Channel to pin map

| Channel | Connector | Nano pin | PWM timer (Nano) | four-tone firmware |
| ------- | --------- | -------- | ---------------- | ------------------ |
| 1 | J11, FAN1 | D3 | Timer2, ~490 Hz | pipe 1 |
| 2 | J12, FAN2 | D5 | Timer0, ~980 Hz | pipe 2 |
| 3 | J13, FAN3 | D6 | Timer0, ~980 Hz | pipe 3 |
| 4 | J14, FAN4 | D9 | Timer1, ~490 Hz | pipe 4 |
| 5 | J15, FAN5 | D10 | Timer1, ~490 Hz | spare |
| 6 | J16, FAN6 | D11 | Timer2, ~490 Hz | spare |

Channels follow the order of the pins along the Nano's header, so the six gate
traces fan out without crossing. D13 is avoided: it has no PWM, and the
bootloader flashes its LED at every reset, which would blip a fan.

## Layout

- **Board:** 130 x 70 mm, 2 layers, 2 mm corner radius, M3 holes 4 mm in from
  each corner.
- **Edges:** fan connectors along the bottom edge, 19 mm apart, each channel's
  parts directly behind its connector. Power terminal on the left edge, wire
  entry facing out, +12 V at the top. Nano sockets along the top right with the
  USB end at the right edge.
- **Nano sockets:** J2 pin k is Nano pin k; J3 pin k is Nano pin 31-k. The
  placement was checked pad for pad against KiCad's `Module:Arduino_Nano`
  footprint.
- **Copper:** GND pours on both layers, stitched with vias. The `Power` net class
  (+12 V, +5 V, GND, FANn_DRV) uses 0.8 mm tracks with 0.25 mm clearance;
  everything else is 0.3 mm with 0.2 mm clearance.
- **Silkscreen:** board name and revision, the licence (CERN-OHL-S-2.0), and the
  source location `github.com/ideocentric/four-tone`, which CERN-OHL-S asks
  products to carry. The ensō house mark sits beside that block
  (source: [`../art/enso-oro.svg`](../art/README.md)). FAN1-FAN6 labels are on
  the board-edge side of the connectors with + beside pin 1, and an outline of
  the Nano's USB connector shows which way round the Nano goes.
- **Checks:** ERC 0 violations; DRC 0 violations, 0 unconnected, 0 schematic
  parity issues (KiCad 9.0.6).

## Known limitations of rev A

- **J1 footprint:** the layout uses KiCad's Phoenix MKDS 1.5 5.08 mm footprint for
  the DB128V-5.08-4P terminal in the BOM (C2915641). Compare the hole size and
  body outline with the real part when the boards arrive.
- **Brushless fans on PWM:** 2-wire brushless fans have their own driver inside.
  Switching their supply with PWM can make them stall or tick at low duty, and
  the ~490 Hz PWM can be audible. The firmware only ramps briefly (250 ms), but
  test one fan before relying on low duty cycles.
- **Fan lead length:** the fans used here have 11" (280 mm) leads, so the board
  has to sit within about 250 mm of each fan once slack is allowed for.
