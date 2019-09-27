#pragma once

#include "visualizer.h"

namespace illuminate {

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

  void Reset() {
    started_ = false;
    start_time_ = 0;
  }

  virtual ::std::string name() = 0;

 protected:
  int number_of_leds() { return number_of_leds_; }

 private:
  int number_of_leds_;

  bool started_;
  double start_time_;
};

}
