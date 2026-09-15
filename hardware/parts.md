# Parts

## Purchased

| Qty | Part | Specs | Source |
| --- | ---- | ----- | ------ |
| 4 | UMLIFE 5015 blower fan, 12 V version | Label `DF5015FAN DC12V 0.18A`. 50 x 50 x 15 mm, 19.5 mm outlet, 5700 RPM, 25 dBA, oil bearing, 2-pin PH2.5 connector, ~30 cm lead. | [Amazon B083HQGJBR](https://www.amazon.com/dp/B083HQGJBR); dimensioned drawings are in the listing's images |
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
| 1 | Driver PCB | `pcb/` (not yet designed) |

## PCB requirements

Known constraints for the board the Arduino plugs into. Component choices are
not made yet.

- **Fan power:** 12 V output of the supply. Four fans at 0.18 A each is 0.72 A
  total, well inside the 7 A rating.
- **Nano socket:** two 1x15 female headers, 0.1" pitch, rows 0.6" (15.24 mm)
  apart, so the Nano plugs in and can be swapped. KiCad ships a matching
  symbol (`MCU_Module:Arduino_Nano_v3.x`) and footprint
  (`Module:Arduino_Nano`).
- **Logic power:** 5 V output of the supply feeds the Nano's `+5V` pin
  directly, bypassing its regulator. The Nano reference design has a Schottky
  diode on USB VBUS, so the supply cannot back-feed the computer when USB is
  plugged in for programming. Clones vary; check the diode is present on the
  boards actually used. Do not also feed `VIN`.
- **Common ground:** the 5 V and 12 V outputs must share ground, since the fan
  switches are on the low side. Confirm with a meter on the supply.
- **Four fan channels,** each: logic-level N-channel MOSFET on the fan's
  ground side, flyback diode across the fan, gate resistor, 10k gate
  pull-down, and a 2-pin JST PH2.5 header so the fans plug straight in.
- **Arduino pins** (from `firmware/include/sequence.h`): D10, D9, D6, D5, in
  pipe order. All four are hardware PWM on the Nano and on the Nano Every.
  D13 is avoided on purpose: no PWM, and the bootloader flashes its LED at
  every reset, which would blip a fan. On the Nano, D5/D6 PWM at ~980 Hz
  (Timer0) and D9/D10 at ~490 Hz (Timer1).
- **PWM behaviour:** the firmware ramps each fan over 250 ms with
  `analogWrite()`. Breadboard-test one fan first: 2-wire brushless fans can
  stall or tick at low duty, and the default ~490 Hz PWM is audible.
