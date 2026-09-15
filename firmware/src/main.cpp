#include <Arduino.h>
#include "sequence.h"

Sequence sequence;

void setup() {
  Serial.begin(9600);
  sequence.begin();
  sequence.setBeatDuration(50.0);
}

void loop() {
  sequence.update();
}
