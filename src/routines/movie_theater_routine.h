#pragma once

#include "routine.h"

#include <cmath>
#include <iostream>

namespace illuminate {
namespace routines {
namespace {
static const int kSpread = 10;
static const int kTimeDivisor = 3;
} // namespace

class MovieTheaterRoutine : public Routine {
 public:
  MovieTheaterRoutine(int number_of_leds) :
      Routine(number_of_leds),
      frame_(0) {}

  void DrawFrame(Visualizer &visualizer) {
    for (int i = 0; i < number_of_leds(); i++) {
      int color = kBlue;

      if (((i + frame_ / kTimeDivisor) / kSpread) % 2 == 0) {
        color = kWhite;
      } else {
        color = kBlue;
      }

      visualizer.SetLed(i, color);
    }

    frame_++;
  }

  ::std::string name() { return "movie_theater"; }

 private:
  int frame_;
};

} // namespace routines
} // namespace illuminate
