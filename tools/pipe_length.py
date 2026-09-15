#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Matt Comeione
# SPDX-License-Identifier: GPL-3.0-or-later
"""Pipe length calculator for the four-tone voices.

A flue pipe sounds at a frequency set by its effective acoustic length, which
is the cut pipe plus a correction for the head joint and the open ends:

    open far end:     f = v / (2 * (L + C))
    stopped far end:  f = v / (4 * (L + C))

C depends on the head joint geometry and cannot be predicted reliably, so it is
measured: cut one test pipe long, measure the note it plays with a tuner, and
give both to --calibrate. The tool solves for C and then gives the cut length
for each target note. Cut long and trim, since a pipe can only get shorter.

    python3 tools/pipe_length.py --calibrate 600 262.1 C5 E5 G5 C6
    python3 tools/pipe_length.py --calibrate 600 262.1 --temp 18 A4 440
    python3 tools/pipe_length.py --info C5 E5 G5 C6

Notes are scientific pitch names (A4 = 440 Hz, sharps as C#5, flats as Eb5)
or plain frequencies in Hz.
"""
import argparse
import math
import re
import sys

NOTE_INDEX = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def speed_of_sound(temp_c):
    """Speed of sound in dry air, m/s."""
    return 331.3 * math.sqrt(1 + temp_c / 273.15)


def parse_note(text, a4=440.0):
    """Return (label, frequency in Hz) for 'C#5', 'Eb4', 'A4' or '440'."""
    try:
        hz = float(text)
        return f"{hz:g} Hz", hz
    except ValueError:
        pass
    m = re.fullmatch(r"([A-Ga-g])([#b]?)(-?\d)", text)
    if not m:
        raise ValueError(f"not a note or frequency: {text!r}")
    letter, accidental, octave = m.group(1).upper(), m.group(2), int(m.group(3))
    semitone = NOTE_INDEX[letter] + {"#": 1, "b": -1, "": 0}[accidental]
    midi = 12 * (octave + 1) + semitone
    return f"{letter}{accidental}{octave}", a4 * 2 ** ((midi - 69) / 12)


def acoustic_length_mm(freq, v, stopped):
    return v / ((4 if stopped else 2) * freq) * 1000


def cents(f, ref):
    return 1200 * math.log2(f / ref)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("notes", nargs="+", help="target notes (C5, Eb5) or frequencies in Hz")
    ap.add_argument("--calibrate", nargs=2, type=float, metavar=("LENGTH_MM", "MEASURED_HZ"),
                    help="a test pipe's cut length and the frequency it plays")
    ap.add_argument("--info", action="store_true",
                    help="only show frequencies and acoustic lengths, no calibration")
    ap.add_argument("--temp", type=float, default=20.0, help="air temperature, deg C (default 20)")
    ap.add_argument("--stopped", action="store_true", help="far end of the pipe is capped")
    ap.add_argument("--a4", type=float, default=440.0, help="tuning reference (default 440)")
    a = ap.parse_args(argv)

    if not a.info and not a.calibrate:
        ap.error("give --calibrate LENGTH_MM MEASURED_HZ, or --info")

    v = speed_of_sound(a.temp)
    targets = [parse_note(n, a.a4) for n in a.notes]
    print(f"speed of sound {v:.1f} m/s at {a.temp:g} C, "
          f"{'stopped' if a.stopped else 'open'} far end, A4 = {a.a4:g} Hz")

    if a.info:
        print(f"\n{'note':<8}{'Hz':>9}{'acoustic length mm':>21}")
        for label, f in targets:
            print(f"{label:<8}{f:>9.2f}{acoustic_length_mm(f, v, a.stopped):>21.1f}")
        return 0

    test_len, test_hz = a.calibrate
    correction = acoustic_length_mm(test_hz, v, a.stopped) - test_len
    print(f"calibration: {test_len:g} mm pipe plays {test_hz:g} Hz -> correction {correction:.1f} mm")
    if correction < 0:
        print("  warning: negative correction. Check the measurement, the far-end setting,"
              " and that the tuner did not read an overtone.", file=sys.stderr)

    print(f"\n{'note':<8}{'Hz':>9}{'cut length mm':>16}{'cut length in':>16}")
    for label, f in targets:
        cut = acoustic_length_mm(f, v, a.stopped) - correction
        flag = "  (shorter than the correction: not playable)" if cut <= 0 else ""
        print(f"{label:<8}{f:>9.2f}{cut:>16.1f}{cut / 25.4:>16.2f}{flag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
