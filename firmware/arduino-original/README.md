# Original sketch

`organ/` is the Arduino IDE sketch the firmware grew from. It is kept for
reference only: PlatformIO does not build it, and the maintained code is in
`../src/` and `../include/`.

## What changed in the conversion

The `.ino` became `src/main.cpp` with `#include <Arduino.h>`, and the classes moved
to `src/` and `include/`. Along the way these bugs were fixed:

- **Pipe indexing:** notes 1-4 indexed a 4-element array directly, so pipe 0
  never played and note 4 wrote past the end of the array. Note *n* now plays
  `pipes[n - 1]`.
- **Event timing:** the check `next_event >= now` was inverted, so a new event
  fired on every loop.
- **Table sizes:** the phrase, note, motive and duration counts were never set,
  so the sequence never advanced past its first entry.
- **Ramp:** each update added the total time since the note started instead of
  the time since the last update, so ramps accelerated instead of rising
  linearly.
- **First event:** the sequencer advanced before playing, skipping the first
  note. It now plays, then advances.
- **Tempo drift and `millis()` rollover:** events are scheduled from the previous
  event's start using elapsed-time subtraction.
- **Start-up:** pin setup moved from the constructor, which runs before the
  Arduino core initialises, into `Sequence::begin()` called from `setup()`.
- **Pins:** the sketch used D13, D11, D10 and D9. D13 has no PWM and flashes at
  reset, so the pipes now use D3, D5, D6 and D9 to match the driver board.
