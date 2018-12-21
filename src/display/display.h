#pragma once

#include <atomic>
#include <iomanip>
#include <iostream>

#include "src/display/visualizer/led_strip/led_strip.h"
#include "lib/phased_loop/phased_loop.h"

namespace src {
namespace display {
namespace {
constexpr int kFramesPerSecond = 30;
constexpr int kNumberOfLeds = 300;
} // namespace

class Display {
 public:
  Display();

  void Run();
  void RunIteration();
  void Quit();

  enum State {
    STARTUP = 0,
    CONNECTING_TO_SERVER = 1,
    DOWNLOADING_ROUTINES = 2,
    BLANK = 3,
    RUN_ROUTINES = 4,
  };

 private:
  void CheckFps();

  LedStrip strip_;

  ::lib::phased_loop::PhasedLoop phased_loop_;
  ::std::atomic<bool> running_;

  double last_iteration_;

  State state_;
};

} // namespace display
} // namespace src
