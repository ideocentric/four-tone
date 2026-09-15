#include <Arduino.h>
#include "sequence.h"


Sequence::Sequence()
{
  this->phrase_index = 0;
  this->note_index = 0;

  this->motive_index = 0;
  this->duration_index = 0;

  this->setBeatDuration(60);
  this->event_start = 0;
  this->event_duration = 0;
}


// Pin setup lives here rather than in the constructor: a global Sequence is
// constructed before the Arduino core's init() runs.
void Sequence::begin()
{
  for(int i=0; i<this->pipe_count; i++)
  {
    this->pipes[i].setPin(this->pins[i]);
    this->pipes[i].setRateOfChange(RAMP_TIME);
  }
  this->event_start = millis();
  this->event_duration = 0;
}


void Sequence::setBeatDuration(float bpm)
{
  this->beat_duration = round(60.0/bpm * 1000);
}


void Sequence::update()
{
  unsigned long now = millis();
  if(now - this->event_start >= this->event_duration)
  {
    // Play the current event, then advance to the next one.
    unsigned long dur = this->rhythm_sequence[this->motive_index][this->duration_index] * this->beat_duration;
    int note = this->phrase_sequence[this->phrase_index][this->note_index];
    if(note != 0)
    {
      this->pipes[note - 1].on(dur);
    }

    // Advance from the scheduled time, not from now, so tempo does not drift.
    this->event_start += this->event_duration;
    this->event_duration = dur;

    this->note_index++;
    if(this->note_index >= this->note_count)
    {
      this->note_index = 0;
      this->phrase_index++;
      if(this->phrase_index >= this->phrase_count)
      {
        this->phrase_index = 0;
      }
    }

    this->duration_index++;
    if(this->duration_index >= this->duration_count)
    {
      this->duration_index = 0;
      this->motive_index++;
      if(this->motive_index >= this->motive_count)
      {
        this->motive_index = 0;
      }
    }
  }

  for(int i=0; i<this->pipe_count; i++)
  {
    this->pipes[i].update();
    Serial.print(i);
    Serial.print(":");
    Serial.print(this->pipes[i].getVoltage());
    if(i+1 < this->pipe_count)
    {
      Serial.print(",");
    }
    else
    {
      Serial.println("");
    }
  }
}
