#include <Arduino.h>
#include "pipe.h"

Pipe::Pipe()
{
  this->pin = 0;
  this->voltage = 0.0;
  this->rate_of_change = 0.0;
  this->start = 0;
  this->duration = 0;
  this->last_update = 0;
  this->running = false;
}


// ramp_time is the time it takes to go from 0->255 in seconds
void Pipe::setRateOfChange(float ramp_time)
{
  this->rate_of_change = 255.0 / (ramp_time * 1000);
}


void Pipe::setPin(byte pin)
{
  this->pin = pin;
  pinMode(this->pin, OUTPUT);
  this->last_update = millis();
}


void Pipe::update()
{
  unsigned long now = millis();

  // Step by the time since the previous update so the ramp is linear.
  float step = this->rate_of_change * (now - this->last_update);
  this->last_update = now;

  // Elapsed-time subtraction stays correct across the millis() rollover.
  if(this->running && now - this->start >= this->duration)
  {
    this->running = false;
  }

  if(this->running)
  {
    this->voltage += step;
    if(this->voltage > 255.0)
    {
      this->voltage = 255.0;
    }
  }
  else
  {
    this->voltage -= step;
    if(this->voltage < 0.0)
    {
      this->voltage = 0.0;
    }
  }

  analogWrite(this->pin, round(this->voltage));
}


void Pipe::on(unsigned long duration)
{
  this->start = millis();
  this->duration = duration;
  this->running = true;
}


int Pipe::getVoltage()
{
  return this->voltage;
}
