# Tuning the pipes

Every four-tone voice uses the same head joint, fan and 2" PVC pipe. Only the length of
the pipe changes, and that length sets the note. This guide finds the length for
each note by measuring one test pipe, then cutting the rest long and trimming to
pitch.

You need a hacksaw or pipe cutter, a tape measure, and a tuner or tuner app that
shows frequency in Hz.

## How length sets pitch

A pipe open at the far end sounds at

```
f = v / (2 x L_eff)
```

where `v` is the speed of sound (about 343 m/s at 20 °C) and `L_eff` is the
effective acoustic length. `L_eff` is longer than the pipe you cut, because the
head joint and the open ends add to it:

```
L_eff = L_cut + C
```

The correction `C` depends on the head joint's window, labium and bore, so it is
measured rather than calculated. Once `C` is known, the cut length for any note
follows. Halving `L_eff` raises the note an octave.

If the far end is capped, the pipe sounds an octave lower, `f = v / (4 x L_eff)`.
The calculator handles both.

## 1. Calibrate with a test pipe

1. Cut a test pipe about 600 mm long, square and deburred. Write down its exact
   length.
2. Fit it to a head joint and fan and run the fan at full speed. The firmware ramps each
   note to full, or you can connect the fan straight to 12 V for this test.
3. Read the steady frequency on the tuner. If the reading jumps an octave as the
   fan comes up to speed, the pipe is overblowing; note the lower, fundamental
   frequency.
4. Note the room temperature. The speed of sound, and so the pitch, rises with
   temperature.

## 2. Calculate the cut lengths

Run the calculator with the test pipe and the notes you want:

```
python3 tools/pipe_length.py --calibrate 600 268.1 --temp 20 C5 E5 G5 C6
```

`600 268.1` is the test pipe's length in mm and the frequency it played. Notes are
written as `C5`, `F#4` or `Bb4` (A4 = 440 Hz), or as frequencies in Hz. Add
`--stopped` for capped pipes and `--a4 442` for a different reference. The output
gives each note's frequency and cut length in mm and inches.

The correction varies a little with pipe length, so calibrate with a test pipe
near the middle of your range, and treat the results as starting lengths.

## 3. Cut long, then trim

1. Cut each pipe 10 to 15 mm longer than the calculated length. A pipe can be
   shortened but not lengthened.
2. Fit it, play it, and read the tuner.
3. Trim a few millimetres at a time from the far end, keeping the cut square,
   until the note is in tune. Each cut raises the pitch.
4. Mark each finished pipe with its note.

As a guide to how much to trim: near 500 Hz, 1 mm of effective length is about
5 cents, and higher notes move more per millimetre than lower ones.

## Things that move the pitch

- **Blowing pressure:** flue pipes go sharp as the air pressure rises and can jump
  to the octave when overblown. Tune with the fan at the level it plays at, which
  in the firmware is full speed.
- **Temperature:** tune at the temperature the instrument will play in.
- **The head joint seal:** a leak where the pipe meets the head joint's socket, or
  around the fan caddy, changes the pitch and tone. Check both before trimming.

## This build

Target notes and final lengths for the four-tone pipes, filled in once measured:

| Pipe | Board channel | Note | Frequency | Cut length |
| ---- | ------------- | ---- | --------- | ---------- |
| 1 | CH1 | TBD | TBD | TBD |
| 2 | CH2 | TBD | TBD | TBD |
| 3 | CH3 | TBD | TBD | TBD |
| 4 | CH4 | TBD | TBD | TBD |

Calibration: TBD (test pipe length, measured frequency, temperature).
