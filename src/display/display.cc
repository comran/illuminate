#include "display.h"

namespace src {
namespace display {

Display::Display(int led_override) :
#ifdef RASPI_DEPLOYMENT
    visualizer_(new LedStrip(kNumberOfLeds)),
#else
    visualizer_(new Simulator(kNumberOfLeds)),
#endif
    phased_loop_(kFramesPerSecond),
    running_(false),
    last_iteration_(::std::numeric_limits<double>::infinity()),
    state_(STARTUP),
    current_routine_(-1),
    client_(kServerUrl),
    programmed_routine_(kNumberOfLeds),
    led_override_(led_override),
    current_runtime_(0) {

  dynamic_routines_.push_back(
      new routines::LineHighlightRoutine(kNumberOfLeds));
  dynamic_routines_.push_back(new routines::OutlineRoutine(kNumberOfLeds));
  dynamic_routines_.push_back(new routines::MovieTheaterRoutine(kNumberOfLeds));
  // dynamic_routines_.push_back(new routines::FadeRoutine(kNumberOfLeds));
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

  bool animation_complete = false;

  // Adjust brightness depending on time of night to avoid annoying the guys
  // with windows facing the sign.
  time_t theTime = time(NULL);
  struct tm *aTime = localtime(&theTime);
  int hour = aTime->tm_hour;
  if (hour >= 23 || hour <= 9) {
    // Dim mode.
    visualizer_->set_brightness(0.5);
  } else {
    // Full brightness mode.
    visualizer_->set_brightness(1.0);
  }

  switch (state_) {
    case STARTUP:
      for (int i = 0; i < kNumberOfLeds; i++) {
        visualizer_->SetLed(i, 0, 0, 0);
      }

      next_state = CONNECTING_TO_SERVER;

      break;

    case LED_OVERRIDE:
      static int current = 0;

      for (int i = 0; i < kNumberOfLeds; i++) {
        if (led_override_ == -1) {
          if (current == i) {
            visualizer_->SetLed(i, 0, 255, 0);
          } else {
            visualizer_->SetLed(i, 0, 0, 0);
          }
        } else if (i < led_override_) {
          visualizer_->SetLed(i, 10, 0, 0);
        } else if (i == led_override_) {
          visualizer_->SetLed(i, 255, 255, 255);
        } else {
          visualizer_->SetLed(i, 0, 0, 0);
        }
      }

      if (led_override_ == -1) {
        ::std::cout << current << ::std::endl;
        current = (current + 1) % 550;
      }

      break;

    case CONNECTING_TO_SERVER:
      for (int i = 0; i < kNumberOfLeds; i++) {
        visualizer_->SetLed(i, 0, 0, 100);
      }

      if (client_.connected()) {
        next_state = DOWNLOADING_ROUTINES;
      }

      break;

    case DOWNLOADING_ROUTINES:
      client_.FetchData();
      next_state = WAIT_FOR_DOWNLOAD_TO_COMPLETE;

      break;

    case WAIT_FOR_DOWNLOAD_TO_COMPLETE:
      for (int i = 0; i < kNumberOfLeds; i++) {
        visualizer_->SetLed(i, 0, 0, 255);
      }

      if (!client_.connected()) {
        next_state = CONNECTING_TO_SERVER;
      }

      if (client_.FetchFinished()) {
        visualizer_->SetPixelLayout(client_.pixel_layout());

        animation_complete = true;
      }

      break;

    case BLANK:
      if (client_.routines_order().size() < 1) {
        next_state = RUN_PROGRAMMED_ROUTINE;
      }

      for (int i = 0; i < kNumberOfLeds; i++) {
        visualizer_->SetLed(i, 0, 0, 0);
      }

      break;

    case RUN_PROGRAMMED_ROUTINE:
      if (client_.routines_order().size() < 1) {
        next_state = BLANK;
      }

      programmed_routine_.DrawFrame(*visualizer_);

      if (programmed_routine_.AnimationComplete(current_runtime_)) {
        animation_complete = true;
      }

      break;

    case RUN_DYNAMIC_ROUTINE:
      routines::Routine *dynamic_routine = dynamic_routines_[current_routine_];
      dynamic_routine->DrawFrame(*visualizer_);

      if (dynamic_routine->AnimationComplete(current_runtime_)) {
        animation_complete = true;
      }

      break;
  }

  // Select the next state if the current animation completes.
  if (animation_complete) {
    int all_routines_count =
        client_.routines_order().size() + dynamic_routines_.size();

    current_routine_ = rand() % all_routines_count;

    if (all_routines_count == 0) {
      next_state = BLANK;
    } else if (current_routine_ <
               static_cast<int>(client_.routines_order().size())) {
      // Select a static programmed routine.
      ::std::string routine_to_run = client_.routines_order()[current_routine_];
      programmed_routine_.LoadRoutineFromProto(
          client_.routines()[routine_to_run]);

      current_runtime_ = 30;

      ::std::cout << "Playing routine \"" << routine_to_run
                  << "\" with runtime " << current_runtime_ << ::std::endl;

      next_state = RUN_PROGRAMMED_ROUTINE;
    } else {
      current_routine_ -= client_.routines_order().size();
      dynamic_routines_[current_routine_]->Reset();
      next_state = RUN_DYNAMIC_ROUTINE;

      ::std::cout << "Playing dynamic routine \""
                  << dynamic_routines_[current_routine_]->name()
                  << "\" with runtime " << current_runtime_ << ::std::endl;
    }
  }

  state_ = next_state;
}

void Display::CheckFps() {
  double current_time =
      ::std::chrono::duration_cast<::std::chrono::nanoseconds>(
          ::std::chrono::system_clock::now().time_since_epoch())
          .count() *
      1e-9;

  if (kPrintFps) {
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
