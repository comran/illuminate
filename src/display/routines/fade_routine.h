#pragma once

#include "routine.h"

#include <cmath>
#include <iostream>

namespace src {
namespace display {
namespace routines {
namespace {
static const int kFadeFrames = 3000;
}

class FadeRoutine : public Routine {
 public:
  FadeRoutine(int number_of_leds) : Routine(number_of_leds), frame_(0) {}

  void DrawFrame(Visualizer &visualizer) {
    double fade_amount = ((double)frame_ / kFadeFrames);
    int r = ((kBlue >> 16) & 0xFF) * fade_amount +
            ((kLightBlue >> 16) & 0xFF) * (1 - fade_amount);
    int g = ((kBlue >> 8) & 0xFF) * fade_amount +
            ((kLightBlue >> 8) & 0xFF) * (1 - fade_amount);
    int b = ((kBlue >> 0) & 0xFF) * fade_amount +
            ((kLightBlue >> 0) & 0xFF) * fade_amount;

    for (int i = 0; i < number_of_leds(); i++) {
      visualizer.SetLed(i, r, g, b);
    }

    frame_++;
  }

  ::std::string name() { return "fade"; }

 private:
  int frame_;
};

} // namespace routines
} // namespace display
} // namespace src
