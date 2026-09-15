#include "Arduino.h"
#include "sequence.h"


Sequence::Sequence()
{
    int i;

    this->phrase_index = 0;
    this->note_index = 0;

    this->motive_index = 0;
    this->duration_index = 0;
    
    this->setBeatDuration(60);
    this->next_event = millis();

    for(i=0; i<this->pipe_count; i++)
    {
      this->pipes[i].setPin(this->pins[i]);
      this->pipes[i].setRateOfChange(RAMP_TIME);
    }
}


void Sequence::setBeatDuration(float bpm)
{
  this->beat_duration = round(60.0/bpm * 1000);
}


void Sequence::update()
{
  Pipe pipe;
  unsigned long dur, t, now;
  now = millis();
  if(this->next_event >= now)
  {
    this->note_index++;
    if(this->note_index >= this->note_count)
    {
      this->note_index = 0;
      this->phrase_index++;
      if(this->phrase_index >= this->phrase_count)
      {
        this->phrase_index =0;
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

    dur = this->rhythm_sequence[this->motive_index][this->duration_index] * this->beat_duration;
    this->next_event = now + dur;
    if(this->phrase_sequence[this->phrase_index][this->note_index] != 0)
    {
      pipes[this->phrase_sequence[this->phrase_index][this->note_index]].on(dur);
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


