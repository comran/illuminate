#pragma once

#include "routine.h"

#include <cmath>
#include <iostream>

namespace src {
namespace display {
namespace routines {

class OutlineRoutine : public Routine {
 public:
  OutlineRoutine(int number_of_leds) :
      Routine(number_of_leds),
      frame_(0),
      split_(0) {}

  void DrawFrame(Visualizer &visualizer) {
    for (int i = 0; i < number_of_leds(); i++) {
      if (split_ < number_of_leds()) {
        if (i < split_) {
          visualizer.SetLed(i, kBlue);
        } else {
          visualizer.SetLed(i, kBlack);
        }
      } else {
        if (i < split_ - number_of_leds()) {
          visualizer.SetLed(i, kBlack);
        } else {
          visualizer.SetLed(i, kBlue);
        }
      }
    }

    frame_++;
    split_ = (split_ + 1) % (number_of_leds() * 2);
  }

  ::std::string name() { return "outline_routine"; }

 private:
  double GetRand() { return ((double)rand() / (RAND_MAX)); }

  int frame_;
  int split_;
};

} // namespace routines
} // namespace display
} // namespace src
