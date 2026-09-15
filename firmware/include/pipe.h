// SPDX-FileCopyrightText: 2024-2026 Matt Comeione
// SPDX-License-Identifier: GPL-3.0-or-later

#ifndef Pipe_h
#define Pipe_h

#include <Arduino.h>

class Pipe
{
  private:
    byte pin;
    float voltage;            // PWM level, 0.0 to 255.0
    float rate_of_change;     // PWM steps per millisecond
    unsigned long start;
    unsigned long duration;
    unsigned long last_update;
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
