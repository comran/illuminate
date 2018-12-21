#include "display.h"

namespace src {
namespace display {

Display::Display() :
#ifdef RASPI_DEPLOYMENT
    visualizer_(new LedStrip(kNumberOfLeds)),
#else
    visualizer_(new StdoutVisual(kNumberOfLeds)),
#endif
    phased_loop_(kFramesPerSecond),
    running_(false),
    last_iteration_(::std::numeric_limits<double>::infinity()),
    state_(STARTUP) {
}

void Display::Run() {
  running_ = true;

  while (running_) {
    RunIteration();
    phased_loop_.SleepUntilNext();
  }
}

void Display::RunIteration() {
  CheckFps();

  State next_state;

  for (int i = 0; i < kNumberOfLeds; i++) {
    visualizer_->SetLed(i, 255, 0, 0);
  }

  static int i = 0;
  i++;
  visualizer_->SetLed(i % kNumberOfLeds, 0, 0, 255);

  if(!visualizer_->Render()) {
    Quit();
  }

  switch (state_) {
    case STARTUP:
      next_state = CONNECTING_TO_SERVER;

      break;

    case CONNECTING_TO_SERVER:

      break;

    case DOWNLOADING_ROUTINES:

      break;

    case BLANK:

      break;

    case RUN_ROUTINES:

      break;
  }

  state_ = next_state;
}

void Display::CheckFps() {
  double current_time =
      ::std::chrono::duration_cast<::std::chrono::nanoseconds>(
          ::std::chrono::system_clock::now().time_since_epoch())
          .count() *
      1e-9;

  double current_fps =
      last_iteration_ == ::std::numeric_limits<double>::infinity()
          ? 0
          : 1.0 / (current_time - last_iteration_);

  ::std::cout << "Frame FPS: " << ::std::fixed << ::std::setprecision(1)
              << current_fps << ::std::endl;

  last_iteration_ = current_time;
}

void Display::Quit() { running_ = false; }

} // namespace display
} // namespace src