#pragma once

#include "routine.h"

#include <cmath>
#include <iostream>

namespace src {
namespace display {
namespace routines {
namespace {
static const int kBlueLeds = 210;
static const int kWhiteLeds = 384;
} // namespace

class TdxRoutine : public Routine {
 public:
  TdxRoutine(int number_of_leds) : Routine(number_of_leds) {}

  void DrawFrame(Visualizer &visualizer) {
    for (int i = 0; i < number_of_leds(); i++) {
      if (i <= kBlueLeds) {
        visualizer.SetLed(i, kBlue);
      } else if (i <= kWhiteLeds) {
        visualizer.SetLed(i, kWhite);
      } else {
        visualizer.SetLed(i, kDimWhite);
      }
    }
  }

  ::std::string name() { return "tdx_routine"; }
};

} // namespace routines
} // namespace display
} // namespace src
