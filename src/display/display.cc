#include "display.h"

namespace src {
namespace display {

Display::Display() :
#ifdef RASPI_DEPLOYMENT
    visualizer_(new LedStrip(kNumberOfLeds)),
#else
    visualizer_(new Simulator(kNumberOfLeds)),
#endif
    phased_loop_(kFramesPerSecond),
    running_(false),
    last_iteration_(::std::numeric_limits<double>::infinity()),
    state_(STARTUP),
    client_(kServerUrl) {
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

  State next_state = state_;

  if (!visualizer_->Render()) {
    Quit();
  }

  switch (state_) {
    case STARTUP:
      for (int i = 0; i < kNumberOfLeds; i++) {
        visualizer_->SetLed(i, 0, 0, 0);
      }

      next_state = CONNECTING_TO_SERVER;

      break;

    case CONNECTING_TO_SERVER:
      for (int i = 0; i < kNumberOfLeds; i++) {
        visualizer_->SetLed(i, 255, 0, 0);
      }

      if(client_.connected()) {
        next_state = DOWNLOADING_ROUTINES;
      }

      break;

    case DOWNLOADING_ROUTINES:
      client_.FetchData();
      next_state = WAIT_FOR_DOWNLOAD_TO_COMPLETE;

      break;

    case WAIT_FOR_DOWNLOAD_TO_COMPLETE:
      for (int i = 0; i < kNumberOfLeds; i++) {
        visualizer_->SetLed(i, 255, 255, 0);
      }

      if(!client_.connected()) {
        next_state = CONNECTING_TO_SERVER;
      }

      if(client_.got_pixel_layout()) {
        visualizer_->SetPixelLayout(client_.pixel_layout());
        next_state = RUN_ROUTINES;
      }

      break;

    case BLANK:
      for (int i = 0; i < kNumberOfLeds; i++) {
        visualizer_->SetLed(i, 0, 0, 0);
      }

      break;

    case RUN_ROUTINES:
      for (int i = 0; i < kNumberOfLeds; i++) {
        visualizer_->SetLed(i, 0, 255, 0);
      }

      if(!client_.connected()) {
        next_state = CONNECTING_TO_SERVER;
      }
      
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

  if(kPrintFps) {
    double current_fps =
        last_iteration_ == ::std::numeric_limits<double>::infinity()
            ? 0
            : 1.0 / (current_time - last_iteration_);

    ::std::cout << "Frame FPS: " << ::std::fixed << ::std::setprecision(1)
                << current_fps << ::std::endl;
  }
  
  last_iteration_ = current_time;
}

void Display::Quit() { running_ = false; }

} // namespace display
} // namespace src