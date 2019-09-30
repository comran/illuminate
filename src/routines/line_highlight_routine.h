#pragma once

#include "routine.h"

#include <cmath>
#include <iostream>

namespace illuminate {
namespace routines {

class LineHighlightRoutine : public Routine {
 public:
  LineHighlightRoutine(int number_of_leds) :
      Routine(number_of_leds),
      frame_(0) {}

  void DrawFrame(Visualizer &visualizer) {
    for (int i = 0; i < number_of_leds(); i++) {
      int color = kBlue;

      if (::std::abs((frame_ % number_of_leds()) - i) < 10) {
        color = kWhite;
      }

      visualizer.SetLed(i, color);
    }

    frame_++;
  }

  ::std::string name() { return "line_highlight"; }

 private:
  int frame_;
};

} // namespace routines
} // namespace illuminate
