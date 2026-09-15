#include "Arduino.h"
#include "pipe.h"
#include "sequence.h"

Sequence sequence;

void setup() {
  // put your setup code here, to run once:
  sequence.setBeatDuration(50.0);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  sequence.update();
}
