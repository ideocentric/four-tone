// SPDX-FileCopyrightText: 2026 Matt Comeione
// SPDX-License-Identifier: GPL-3.0-or-later
//
// Bench test for the six fan driver board. Build and upload with:
//
//     pio run -e selftest -t upload
//     pio device monitor          (9600 baud)
//
// It walks the six channels one at a time and says over serial what it is
// doing, so the indicator LEDs and any connected fan can be checked against it.
// Deliberately standalone: it shares no code with the music firmware, so a fault
// here points at the board, not at the sequencer.
//
// Each channel gets three steps:
//   1. full on, so the LED should be at its brightest and a fan should spin up
//   2. a slow PWM sweep up and down, which is where 2-wire brushless fans are
//      most likely to tick, stall or refuse to start
//   3. off
//
// Then all six run together, which is the largest current the board will draw.

#include <Arduino.h>

const uint8_t PINS[] = {3, 5, 6, 9, 10, 11};   // channels 1-6, J11-J16
const uint8_t CHANNELS = sizeof(PINS) / sizeof(PINS[0]);

const unsigned long FULL_MS = 2000;    // step 1: full on
const unsigned long SWEEP_MS = 1500;   // step 2: each direction of the sweep
const unsigned long OFF_MS = 800;      // step 3: off
const unsigned long ALL_MS = 2000;     // all channels together
const unsigned long PAUSE_MS = 3000;   // between passes

unsigned long pass = 0;

void allOff() {
  for (uint8_t i = 0; i < CHANNELS; i++) {
    analogWrite(PINS[i], 0);
  }
}

// Ramp one channel between two levels over the given time, in 20 ms steps.
void sweep(uint8_t pin, int from, int to, unsigned long ms) {
  const unsigned long step = 20;
  const unsigned long steps = ms / step;
  for (unsigned long i = 0; i <= steps; i++) {
    analogWrite(pin, from + (int)((long)(to - from) * (long)i / (long)steps));
    delay(step);
  }
}

void setup() {
  Serial.begin(9600);
  for (uint8_t i = 0; i < CHANNELS; i++) {
    pinMode(PINS[i], OUTPUT);
  }
  allOff();
  delay(500);
  Serial.println();
  Serial.println(F("four-tone six fan driver: self test"));
  Serial.println(F("channel  pin  connector"));
  for (uint8_t i = 0; i < CHANNELS; i++) {
    Serial.print(F("  CH"));
    Serial.print(i + 1);
    Serial.print(F("      D"));
    Serial.print(PINS[i]);
    Serial.print(F("   J"));
    Serial.println(11 + i);
  }
  Serial.println(F("Every channel should be off now: no LED lit."));
  Serial.println();
}

void loop() {
  pass++;
  Serial.print(F("--- pass "));
  Serial.println(pass);

  for (uint8_t i = 0; i < CHANNELS; i++) {
    const uint8_t pin = PINS[i];

    Serial.print(F("CH"));
    Serial.print(i + 1);
    Serial.print(F(" (D"));
    Serial.print(pin);
    Serial.print(F(", J"));
    Serial.print(11 + i);
    Serial.println(F("): full on"));
    analogWrite(pin, 255);
    delay(FULL_MS);

    Serial.println(F("        sweep down to off, then back up"));
    sweep(pin, 255, 0, SWEEP_MS);
    sweep(pin, 0, 255, SWEEP_MS);

    Serial.println(F("        off"));
    analogWrite(pin, 0);
    delay(OFF_MS);
  }

  Serial.println(F("all six channels on together"));
  for (uint8_t i = 0; i < CHANNELS; i++) {
    analogWrite(PINS[i], 255);
  }
  delay(ALL_MS);
  allOff();

  Serial.println(F("all off; pausing"));
  Serial.println();
  delay(PAUSE_MS);
}
