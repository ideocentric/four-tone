# Parts

Everything needed to build four-tone. The driver board's own component list is in
[`pcb/README.md`](pcb/README.md#bom).

## Purchased

| Qty | Part | Specs | Source |
| --- | ---- | ----- | ------ |
| 4 | UMLIFE 5015 blower fan, 12 V version | Label `DF5015FAN DC12V 0.18A`. 50 x 50 x 15 mm, 19.5 mm outlet, 5700 RPM, 25 dBA, oil bearing. 2-pin plug, pitch measured 2.54 mm (JST XH style; the listing says "PH2.5"). Lead 11" (280 mm). | [Amazon B083HQGJBR](https://www.amazon.com/dp/B083HQGJBR); dimensioned drawings are in the listing's images |
| 1 | Arcity arcade switching power supply | Outputs +5 V/8 A, +12 V/7 A, +24 V/5 A. Input 110/220 V switchable. OVP, OCP, SCP, OTP. 160 x 98 x 38 mm. | [Amazon B07RT54H9V](https://www.amazon.com/dp/B07RT54H9V) (specs from the listing, not yet checked against the unit's label) |
| 1 | Arduino Nano, classic (A000005, ATmega328P) | 16 MHz, 5 V logic, 32 KB flash, 2 KB SRAM, 6 PWM pins (D3, D5, D6, D9, D10, D11), Mini-B USB. | [Arduino Store](https://store-usa.arduino.cc/collections/nano-family/products/arduino-nano) |
| 4 | 2" PVC pipe | Same stock for every voice; cut to length per note. Tested with the head joint. The head joint bore (53 mm) matches the 52.5 mm inside diameter of Schedule 40. | Hardware store |
| - | Wire for the supply and mains | Sized for the supply's terminals; a mains lead with earth. | |

The supply's 24 V output is unused.

A Nano Every (ABX00033, ATmega4809, [Amazon B07WWK29XF](https://www.amazon.com/dp/B07WWK29XF))
can stand in for the Nano. It has 5 PWM pins, not the 6 its listing claims
(D3, D5, D6, D9, D10 per Arduino's datasheet and megaAVR core), which still
covers the four pipes and channel 5. It needs `platform = atmelmegaavr` and
`board = nano_every` in `platformio.ini`.

## Made

| Qty | Part | Source |
| --- | ---- | ------ |
| 4 | Head joint | [`../mechanical/cad/fan_organ_pipe_rev_02.FCStd`](../mechanical/README.md), 3D printed |
| 4 | Fan caddy | [`../mechanical/cad/fan_mount_rev-01.FCStd`](../mechanical/README.md), 3D printed |
| 4 | Pipe, cut to pitch | See the [tuning guide](../docs/tuning.md) |
| 1 | Open-bottom wooden enclosure | [`../mechanical/enclosure/`](../mechanical/README.md#enclosure) |
| 1 | Six fan driver PCB, rev A | [`pcb/`](pcb/README.md), ordered from JLCPCB |
