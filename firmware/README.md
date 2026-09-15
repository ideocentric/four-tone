# Firmware

The firmware runs on a classic Arduino Nano (ATmega328P) plugged into the
[six fan driver](../hardware/pcb/README.md). It plays an endless sequence on
four pipes, fading each fan up at the start of a note and down after it.

| Path | Contents |
| ---- | -------- |
| `src/main.cpp` | `setup()` and `loop()`: starts serial, sets the tempo, runs the sequencer |
| `include/sequence.h`, `src/sequence.cpp` | The sequencer: pin map, note and rhythm tables, timing |
| `include/pipe.h`, `src/pipe.cpp` | One fan: PWM level, ramp up and down, note duration |
| `arduino-original/` | The original Arduino IDE sketch, kept for reference only |
| `../platformio.ini` | Build configuration |

## Building and uploading

### PlatformIO (command line)

1. Install [PlatformIO Core](https://docs.platformio.org/en/latest/core/installation/index.html),
   for example `brew install platformio` or `pipx install platformio`.
2. From the repository root:

   ```
   pio run                 # build
   pio run -t upload       # build and upload over USB
   pio device monitor      # serial output, 9600 baud
   ```

3. If the upload fails with `not in sync`, the Nano has the old bootloader, which
   many clones still ship with. Use `pio run -e nano_old -t upload`.

### CLion

Install the **PlatformIO for CLion** plugin, open the repository root, and use the
PlatformIO run configurations (Build, Upload, Monitor) that CLion creates from
`platformio.ini`.

### Arduino IDE

The sources are plain C++, so the Arduino IDE can build them too: create a sketch
folder, copy everything from `src/` and `include/` into it, and add an `.ino` file
named after the folder (it can contain just a comment). Select **Arduino Nano** and
the right processor (**ATmega328P** or **ATmega328P (Old Bootloader)**).

The firmware compiles to 4828 bytes of flash (15%) and 906 bytes of RAM (44%).

## How the sequence works

The sequencer steps through **events**. Each event plays one pipe, or rests, for
a number of beats. Two tables drive it, both in `include/sequence.h`.

**Phrases** (`phrase_sequence`): 24 rows of five entries. The first four entries
of each row are the pipes 1-4 in some order, and the fifth is `0`, a rest. The 24
rows are every possible ordering of the four pipes, each used once.

**Motives** (`rhythm_sequence`): 5 rows of five beat counts. Every row has four
1-beat events and one 2-beat event, and the long event moves one place later in
each row.

Phrases and motives advance together, one row per bar of five events, so bar *n*
uses phrase *n* mod 24 with motive *n* mod 5. A bar is 6 beats. Because 24 and 5
share no factor, it takes 120 bars before the same phrase meets the same rhythm
again.

At the default 50 BPM (set in `main.cpp`):

| Unit | Length |
| ---- | ------ |
| Beat | 1.2 s |
| Bar (5 events, 6 beats) | 7.2 s |
| Full cycle (120 bars) | 14.4 min |

**Fans:** when an event starts, its fan ramps from off to full over 250 ms
(`RAMP_TIME`), stays on for the event's duration, then ramps back down over
250 ms. The fade-out runs into the next event, so consecutive notes overlap
slightly. Rests leave all fans fading or off.

Timing is scheduled from the previous event's start rather than from "now", so the
tempo does not drift even though the serial output slows the loop down.

## Pin map

| Pipe | Board channel | Nano pin |
| ---- | ------------- | -------- |
| 1 | CH1, FAN1 (J11) | D3 |
| 2 | CH2, FAN2 (J12) | D5 |
| 3 | CH3, FAN3 (J13) | D6 |
| 4 | CH4, FAN4 (J14) | D9 |

Channels 5 and 6 (D10, D11) are wired on the board but not used. Set in `pins[]` in
`include/sequence.h`.

## Serial output

At 9600 baud the firmware prints one line per loop with each fan's PWM level,
0 (off) to 255 (full):

```
0:255,1:0,2:0,3:0
```

The numbers before the colons are pipe indexes counted from 0, so `0` is pipe 1.
The format suits the Arduino IDE's **Serial Plotter**, which draws the four fans
as traces and makes the ramps visible.

## Changing the music

All of this is in `include/sequence.h` unless noted.

- **Tempo:** `sequence.setBeatDuration(50.0)` in `src/main.cpp`, in BPM.
- **Notes:** edit `phrase_sequence`. Each entry is a pipe number, 1-4, or `0` for
  a rest.
- **Rhythm:** edit `rhythm_sequence`. Each entry is the event's length in beats.
- **Table sizes:** if you change the number of rows or entries, change
  `NUMBER_OF_PHRASES`, `NUMBER_OF_NOTES`, `NUMBER_OF_MOTIVES` and
  `NUMBER_OF_DURATIONS` to match. Keep `NUMBER_OF_NOTES` equal to
  `NUMBER_OF_DURATIONS`, or notes and rhythms drift out of step within a bar.
- **Fade time:** `RAMP_TIME`, in seconds. A longer ramp softens the attack but
  the pipe speaks later.
- **Using channels 5 and 6:** set `NUMBER_OF_PIPES` to 6, extend `pins[]` to
  `{3,5,6,9,10,11}`, and use pipe numbers 5 and 6 in the phrases.
- **Memory:** the Nano has 2 KB of RAM and the tables are `int` arrays held in
  RAM. Large new tables can run it out; `pio run` prints the RAM use.

## History

The code started as an Arduino IDE sketch (`arduino-original/organ/`) and was
converted to PlatformIO C++ in this repository. The conversion also fixed several
bugs; see [`arduino-original/README.md`](arduino-original/README.md).
