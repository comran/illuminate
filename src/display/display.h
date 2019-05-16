#pragma once

#include <atomic>
#include <iomanip>
#include <iostream>
#include <stdlib.h>
#include <time.h>
#include <vector>

#include "lib/phased_loop/phased_loop.h"
#include "src/display/client/client.h"
#include "src/display/routines/fade_routine.h"
#include "src/display/routines/line_highlight_routine.h"
#include "src/display/routines/movie_theater_routine.h"
#include "src/display/routines/outline_routine.h"
#include "src/display/routines/programmed_routine.h"
#include "src/display/routines/tdx_routine.h"

#ifdef RASPI_DEPLOYMENT
#include "src/display/visualizer/led_strip.h"
#else
#include "src/display/visualizer/simulator.h"
#endif

namespace src {
namespace display {
namespace {
static constexpr int kFramesPerSecond = 30;
static constexpr int kNumberOfLeds = 551;
static const bool kPrintFps = false;
static const int kNumberOfDynamicRoutines = 2;
static const int kBlankBrightness = 0;
static const double kMaxBrightness = 0.9;
static const double kMinBrightness = 0.25;
static const double kDimFadeStartHour = 12 + 9;
static const double kDimFadeEndHour = 12 + 11.5;

#ifdef RASPI_DEPLOYMENT
static const char *const kServerUrl = "http://127.0.0.1:5000";
#else
// static const char *const kServerUrl = "http://comran.org:5000";
static const char *const kServerUrl = "http://localhost:5000";
#endif
} // namespace

class Display {
 public:
  Display(int led_override);

  void Run();
  void RunIteration();
  void Quit();

  enum State {
    STARTUP = 0,
    LED_OVERRIDE = 1,
    CONNECTING_TO_SERVER = 2,
    DOWNLOADING_ROUTINES = 3,
    WAIT_FOR_DOWNLOAD_TO_COMPLETE = 4,
    BLANK = 5,
    RUN_PROGRAMMED_ROUTINE = 6,
    RUN_DYNAMIC_ROUTINE = 7,
  };

 private:
  void CheckFps();
  double GetBrightness(struct tm *aTime);
  int GetAnimatedRuntime(::std::string routine_to_run);
  bool OverrideOnThursday(struct tm *aTime);
  bool OverrideOnWeekday(struct tm *aTime);
  void SetState(State state);

  Visualizer *visualizer_;

  ::lib::phased_loop::PhasedLoop phased_loop_;
  ::std::atomic<bool> running_;

  double last_iteration_;

  State state_;
  int current_routine_;
  int last_routine_;
  client::Client client_;
  ::std::vector<::src::display::routines::Routine *> dynamic_routines_;
  routines::ProgrammedRoutine programmed_routine_;
  int led_override_;
  double current_runtime_;
};

} // namespace display
} // namespace src
