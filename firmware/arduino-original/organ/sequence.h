#ifndef Sequence_h
#define Sequence_h

#include "Arduino.h"
#include "pipe.h"

#define NUMBER_OF_PINS 7
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
    int beats;
    float ramp_time = RAMP_TIME;
    unsigned long beat_duration;
    unsigned long next_event;

    // micro 
    Pipe pipes[NUMBER_OF_PIPES];
    int pipe_count = NUMBER_OF_PIPES;
    int pins[NUMBER_OF_PINS] = {13,11,10,9,6,5,3};  // Arduino Mini Pins in order of physical layout on board.

    int phrase_count;
    int note_count;
  
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

    int motive_count;
    int duration_count;
    int rhythm_sequence[NUMBER_OF_MOTIVES][NUMBER_OF_DURATIONS] = {
      {1, 2, 1, 1, 1},
      {1, 1, 2, 1, 1},
      {1, 1, 1, 2, 1},
      {1, 1, 1, 1, 2},
      {2, 1, 1, 1, 1}
    };

  public:
    Sequence();
    void setBeatDuration(float bpm);
    void update();
};





#endif