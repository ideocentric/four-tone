#include "Arduino.h"
#include "pipe.h"

Pipe::Pipe()  // ramp_time is the time it takes to go from 0->255 in seconds
{
  //this->pin = pin;
  //pinMode(this->pin, OUTPUT);
  this->voltage = 0.0;
  this->start = millis();
  this->stop = millis();
  this->running = false;
}


void Pipe::setRateOfChange(float ramp_time)
{
  this->rate_of_change = 255.0/(ramp_time * 1000);
}


void Pipe::setPin(byte pin)
{
  this->pin = pin;
  pinMode(this->pin, OUTPUT);
}


void Pipe::update()
{
  // update values
  unsigned long t, now;
  now = millis();

  if(now > this->stop)
  {
    this->running = false;
  }
  
  if(this->running)
  {
    if(this->voltage < 255.0)
    {
      t = now - this->start;
      this->voltage = this->voltage + (this->rate_of_change * t);
      if(this->voltage >= 255.0)
      {
        this->voltage = 255.0;
      }
    }
  }
  else
  {
    if(this->voltage > 0.0)
    {
        t = now - this->stop;
        this->voltage = this->voltage - (this->rate_of_change * t);
        if(this->voltage <= 0.0)
        {
          this->voltage = 0;
        }
    }
  }
  analogWrite(this->pin, round(this->voltage));
}

void Pipe::on(unsigned long duration)
{
  this->start = millis();
  this->stop = this->start + duration;
  this->running = true; 
}

int Pipe::getVoltage()
{
  return this->voltage;
}
