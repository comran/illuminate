#pragma once

#include <atomic>
#include <iomanip>
#include <iostream>

#include "lib/phased_loop/phased_loop.h"
#include "src/display/client/client.h"
#ifdef RASPI_DEPLOYMENT
#include "src/display/visualizer/led_strip.h"
#else
#include "src/display/visualizer/simulator.h"
#endif

namespace src {
namespace display {
namespace {
static constexpr int kFramesPerSecond = 30;
static constexpr int kNumberOfLeds = 265;
static const bool kPrintFps = false;
static const char *const kServerUrl = "http://127.0.0.1:5000";
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
    WAIT_FOR_DOWNLOAD_TO_COMPLETE = 3,
    BLANK = 4,
    RUN_ROUTINES = 5,
  };

 private:
  void CheckFps();

  Visualizer *visualizer_;

  ::lib::phased_loop::PhasedLoop phased_loop_;
  ::std::atomic<bool> running_;

  double last_iteration_;
  int current_routine_;

  State state_;
  client::Client client_;
};

} // namespace display
} // namespace src
