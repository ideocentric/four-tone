#ifndef Pipe_h
#define Pipe_h

#include "Arduino.h"

class Pipe 
{
  private:
    byte pin;
    float voltage;
    float rate_of_change;
    unsigned long start;
    unsigned long stop;
    bool running = false;

  public:
    Pipe();
    void setRateOfChange(float ramp_time);
    void setPin(byte pin);
    void update();
    void on(unsigned long duration);
    int getVoltage();
};

#endif