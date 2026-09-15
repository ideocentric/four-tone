# Parts

## Purchased

| Qty | Part | Specs | Source |
| --- | ---- | ----- | ------ |
| 4 | UMLIFE 5015 blower fan, 12 V version | Label `DF5015FAN DC12V 0.18A`. 50 x 50 x 15 mm, 19.5 mm outlet, 5700 RPM, 25 dBA, oil bearing. 2-pin plug, pitch measured 2.54 mm (JST XH style; the listing says "PH2.5"). Lead 11" (280 mm). | [Amazon B083HQGJBR](https://www.amazon.com/dp/B083HQGJBR); dimensioned drawings are in the listing's images |
| 1 | Arcity arcade switching power supply | Outputs +5 V/8 A, +12 V/7 A, +24 V/5 A. Input 110/220 V switchable. OVP, OCP, SCP, OTP. 160 x 98 x 38 mm. | [Amazon B07RT54H9V](https://www.amazon.com/dp/B07RT54H9V) (specs from the listing, not yet checked against the unit's label) |
| 1 | Arduino Nano, classic (A000005, ATmega328P) | 16 MHz, 5 V logic, 32 KB flash, 2 KB SRAM, 6 PWM pins (D3, D5, D6, D9, D10, D11), Mini-B USB. PlatformIO env `nano` (new bootloader) or `nano_old`. | [Arduino Store](https://store-usa.arduino.cc/collections/nano-family/products/arduino-nano) |

A Nano Every (ABX00033, ATmega4809, [Amazon B07WWK29XF](https://www.amazon.com/dp/B07WWK29XF))
was also bought but is not the target board. It has 5 PWM pins, not the 6 the
listing claims (D3, D5, D6, D9, D10 per Arduino's datasheet and megaAVR core).
The firmware compiles for it and the fan pins are PWM on it too, so it can
stand in, but it needs `platform = atmelmegaavr`, `board = nano_every`.

The 24 V output is unused.

## Fabricated

| Qty | Part | Source |
| --- | ---- | ------ |
| 4 | Beak | `../mechanical/cad/fan_organ_pipe_rev_02.FCStd` |
| 4 | Fan caddy | `../mechanical/cad/fan_mount_rev-01.FCStd` |
| 4 | 2" PVC pipe, cut to pitch | Same stock for all four; length TBD per note |
| 1 | Open-bottom wooden enclosure | `../mechanical/enclosure/` |
| 1 | Driver PCB, rev A | `pcb/four-tone-driver.kicad_sch` (schematic done, layout not started) |

## Driver board, rev A

Arduino Nano carrier with six low-side MOSFET fan channels (four used by this
project, two spare). Intended for JLCPCB fabrication and assembly. LCSC part
numbers are in each symbol's `LCSC` field.

### BOM

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

Availability checked 2026-09-15 through tscircuit's jlcsearch mirror of the
JLCPCB catalogue; every line was in stock. Re-check in JLCPCB's BOM tool when
ordering.

### Circuit

- **Power, J1:** pin 1 +12 V, pin 2 GND, pin 3 +5 V, pin 4 GND, from the
  supply's 12 V and 5 V outputs. The two grounds are joined on the board, so
  the supply's 5 V and 12 V returns must be common. Confirm with a meter.
- **Logic power:** +5 V feeds the Nano's `+5V` pin through J3 pin 4, bypassing
  its regulator. `VIN` is left unconnected. The Nano reference design has a
  Schottky diode on USB VBUS, so the supply cannot back-feed a computer during
  programming. Clones vary; check the boards actually used.
- **Fan channel n:** Nano PWM pin, 1 k to the AO3400A gate, 100 k gate
  pull-down to GND so the fan stays off while the Nano resets or is removed.
  The MOSFET switches the fan's return (J1n pin 2) to GND. An SS14 across the
  fan clamps the lead inductance. A red LED with 4.7 k from +12 V to the
  switched return lights when the channel is on (about 2 mA), and follows the
  PWM ramp. It also lights with no fan plugged in, which helps bench testing.
- **Fan connectors J11-J16:** pin 1 +12 V, pin 2 switched return. Check which
  pin the red lead lands on in the fan's plug before wiring, and mark + on the
  silkscreen during layout.
- **Current:** fans are rated 0.18 A. Design margin is 0.5 A per channel for
  start-up, 3 A for all six. AO3400A at 5 V gate drive is about 30 mOhm, so
  under 10 mW per channel.

### Channel to pin map

| Channel | Connector | Nano pin | PWM timer (Nano) | Firmware |
| ------- | --------- | -------- | ---------------- | -------- |
| 1 | J11 | D10 | Timer1, ~490 Hz | pipe 1 |
| 2 | J12 | D9 | Timer1, ~490 Hz | pipe 2 |
| 3 | J13 | D6 | Timer0, ~980 Hz | pipe 3 |
| 4 | J14 | D5 | Timer0, ~980 Hz | pipe 4 |
| 5 | J15 | D3 | Timer2, ~490 Hz | spare |
| 6 | J16 | D11 | Timer2, ~490 Hz | spare |

D13 is avoided: no PWM, and the bootloader flashes its LED at every reset,
which would blip a fan.

### Layout notes

- **Nano sockets:** J2 pin k is Nano pin k; J3 pin k is Nano pin 31-k. Place
  both with pin 1 on the same row and the rows 15.24 mm apart, matching the
  `Module:Arduino_Nano` footprint (pads 1 and 30). The Nano's USB end is at
  pin 15, so keep that end at a board edge for cable access.
- **J1 footprint:** the schematic uses KiCad's Phoenix MKDS 1.5 5.08 mm
  footprint. Check its hole size and body outline against the LCSC datasheet
  for C2915641 before routing.
- **Fan leads are 11"**, so the board has to sit within about 250 mm of each
  fan once the plug and some slack are allowed for.
- **Traces:** 1 mm for the +12 V bus and GND returns, 0.5 mm for each fan's
  switched return, signal width for gates.

### PWM behaviour

The firmware ramps each fan over 250 ms with `analogWrite()`. Breadboard-test
one fan first: 2-wire brushless fans can stall or tick at low duty, and the
~490 Hz PWM is audible.
