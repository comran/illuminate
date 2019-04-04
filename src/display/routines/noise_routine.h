#pragma once

#include "routine.h"

#include <cmath>
#include <iostream>

namespace src {
namespace display {
namespace routines {

class NoiseRoutine : public Routine {
 public:
  NoiseRoutine(int number_of_leds) : Routine(number_of_leds), frame_(0) {}

  void DrawFrame(Visualizer &visualizer) {
    if (frame_ == 0) {
      for (int i = 0; i < number_of_leds(); i++) {
        visualizer.SetLed(i, kDimBlue);
      }
    } else {
      if (GetRand() > 0.5) {
        visualizer.SetLed(GetRand() * number_of_leds(), kBlue);
      } else {
        visualizer.SetLed(GetRand() * number_of_leds(), kDimBlue);
      }
    }

    frame_++;
  }

 private:
  double GetRand() { return ((double)rand() / (RAND_MAX)); }

  int frame_;
};

} // namespace routines
} // namespace display
} // namespace src
