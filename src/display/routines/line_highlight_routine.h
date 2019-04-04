#pragma once

#include "routine.h"

#include <cmath>
#include <iostream>

namespace src {
namespace display {
namespace routines {

class LineHighlightRoutine : public Routine {
 public:
  LineHighlightRoutine(int number_of_leds) :
      Routine(number_of_leds),
      frame_(0) {}

  void DrawFrame(Visualizer &visualizer) {
    for (int i = 0; i < number_of_leds(); i++) {
      int color = kDimBlue;

      if (::std::abs((frame_ % number_of_leds()) - i) < 10) {
        color = kLightBlue;
      }

      visualizer.SetLed(i, color);
    }

    frame_++;
  }

 private:
  int frame_;
};

} // namespace routines
} // namespace display
} // namespace src
