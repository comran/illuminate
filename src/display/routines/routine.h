#pragma once

#include "src/display/visualizer/visualizer.h"

namespace src {
namespace display {
namespace routines {
namespace {
static const int kLightBlue = 0x4444FF;
static const int kBlue = 0x0000FF;
static const int kDimBlue = 0x0000AA;
static const int kWhite = 0xFFFFFF;
} // namespace

class Routine {
 public:
  Routine(int number_of_leds) :
      number_of_leds_(number_of_leds),
      started_(false) {}

  virtual void DrawFrame(Visualizer &visualizer) = 0;

  bool AnimationComplete(double runtime) {
    double current_time =
        ::std::chrono::duration_cast<::std::chrono::nanoseconds>(
            ::std::chrono::system_clock::now().time_since_epoch())
            .count() *
        1e-9;

    if (!started_) {
      start_time_ = current_time;
      started_ = true;
    }

    if (current_time < start_time_ + runtime) {
      return false;
    }

    return true;
  }

 protected:
  void Reset() {
    started_ = false;
    start_time_ = 0;
  }

  int number_of_leds() { return number_of_leds_; }

 private:
  int number_of_leds_;

  bool started_;
  double start_time_;
};

} // namespace routines
} // namespace display
} // namespace src
