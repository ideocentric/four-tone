#ifndef Sequence_h
#define Sequence_h

#include <Arduino.h>
#include "pipe.h"

#define NUMBER_OF_PHRASES 24
#define NUMBER_OF_NOTES 5
#define NUMBER_OF_MOTIVES 5
#define NUMBER_OF_DURATIONS 5
#define NUMBER_OF_PIPES 4
#define RAMP_TIME 0.25

class Sequence
{
  private:
    int phrase_index;
    int note_index;
    int motive_index;
    int duration_index;
    unsigned long beat_duration;
    unsigned long event_start;
    unsigned long event_duration;

    // micro
    Pipe pipes[NUMBER_OF_PIPES];
    int pipe_count = NUMBER_OF_PIPES;
    // Fan pins, in pipe order. All four are hardware PWM on the Arduino Nano
    // (and on the Nano Every), so every fan can ramp.
    int pins[NUMBER_OF_PIPES] = {10,9,6,5};

    int phrase_count = NUMBER_OF_PHRASES;
    int note_count = NUMBER_OF_NOTES;

    // Notes are numbered 1 to NUMBER_OF_PIPES; 0 is a rest.
    int phrase_sequence[NUMBER_OF_PHRASES][NUMBER_OF_NOTES] = {
      {1, 2, 4, 3, 0},
      {4, 3, 1, 2, 0},
      {3, 2, 1, 4, 0},
      {2, 4, 3, 1, 0},
      {3, 1, 4, 2, 0},
      {1, 4, 2, 3, 0},
      {2, 3, 4, 1, 0},
      {4, 1, 3, 2, 0},
      {3, 2, 4, 1, 0},
      {2, 1, 3, 4, 0},
      {1, 3, 4, 2, 0},
      {4, 1, 2, 3, 0},
      {1, 3, 2, 4, 0},
      {3, 4, 2, 1, 0},
      {4, 2, 3, 1, 0},
      {2, 1, 4, 3, 0},
      {4, 3, 2, 1, 0},
      {2, 4, 1, 3, 0},
      {1, 2, 3, 4, 0},
      {3, 4, 1, 2, 0},
      {4, 2, 1, 3, 0},
      {2, 3, 1, 4, 0},
      {1, 4, 3, 2, 0},
      {3, 1, 2, 4, 0}
    };

    int motive_count = NUMBER_OF_MOTIVES;
    int duration_count = NUMBER_OF_DURATIONS;
    int rhythm_sequence[NUMBER_OF_MOTIVES][NUMBER_OF_DURATIONS] = {
      {1, 2, 1, 1, 1},
      {1, 1, 2, 1, 1},
      {1, 1, 1, 2, 1},
      {1, 1, 1, 1, 2},
      {2, 1, 1, 1, 1}
    };

  public:
    Sequence();
    void begin();
    void setBeatDuration(float bpm);
    void update();
};

#endif
