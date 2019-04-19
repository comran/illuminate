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
    last_routine_(-1),
    client_(kServerUrl),
    programmed_routine_(kNumberOfLeds),
    led_override_(led_override),
    current_runtime_(0),
    printed_dimmed_(false) {

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
  time_t theTime = time(NULL);
  struct tm *aTime = localtime(&theTime);
  int hour = aTime->tm_hour;
  int day_of_month = aTime->tm_mday;
  int month = aTime->tm_mon;
  CheckFps();

  State next_state = state_;

  if (!visualizer_->Render()) {
    Quit();
  }

  bool animation_complete = false;

  // Adjust brightness depending on time of night to avoid annoying the guys
  // with windows facing the sign.

  visualizer_->set_brightness(1.0);
  if (hour >= 23 || hour <= 9) {
    // Dim mode.
    visualizer_->set_brightness(0.40);

    if (!printed_dimmed_) {
      ::std::cout << "Late at night; entering dimmed mode." << ::std::endl;
      printed_dimmed_ = true;
    }
  } else {
    // Full brightness mode.
    visualizer_->set_brightness(1.0);
    printed_dimmed_ = false;
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

        ::std::cout << "hour is " << hour << ::std::endl;
        ::std::cout << "day_of_month is " << day_of_month << ::std::endl;
        ::std::cout << "month is " << month << ::std::endl;

        animation_complete = true;
      }

      break;

    case BLANK:
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
  while (animation_complete) {
    bool blank = false;
    if (month == 3) {
      int day;
      int hour_start = 12 + 9;
      int hour_end = 4;

      // TODO: Deal with days that wrap to the next month.

      // Euroclub party.
      day = 19;
      if ((day_of_month == day && hour >= hour_start) ||
          (day_of_month == (day + 1) && hour <= hour_end)) {
        blank = true;
      }

      // Drip or drown.
      day = 20;
      if ((day_of_month == day && hour >= hour_start) ||
          (day_of_month == (day + 1) && hour <= hour_end)) {
        blank = true;
      }
    }

    if (blank) {
      next_state = BLANK;
      break;
    }

    // Override on 420.
    int day = 20;
    if (month == 3 && ((day_of_month == day && hour > 12) ||
                       (day_of_month == (day + 1) && hour < 12))) {
      ::std::string found_routine = "";

      int i = 0;
      for (::std::string routine : client_.routines_order()) {
        if (routine == "rasta") {
          found_routine = routine;
          break;
        }

        i++;
      }

      if (found_routine == "") {
        next_state = BLANK;
      } else {
        next_state = RUN_PROGRAMMED_ROUTINE;
        current_runtime_ = 30;

        programmed_routine_.LoadRoutineFromProto(
            client_.routines()[found_routine]);
      }

      ::std::cout << "Playing " << found_routine << ::std::endl;

      break;
    }

    int all_routines_count =
        client_.routines_order().size() + dynamic_routines_.size();

    current_routine_ = rand() % all_routines_count;

    // Don't repeat routines back-to-back.
    if (current_routine_ == last_routine_) {
      current_routine_ = (current_routine_ + 1) % all_routines_count;
    }

    last_routine_ = current_routine_;

    if (all_routines_count == 0) {
      next_state = BLANK;
      animation_complete = false;
    } else if (current_routine_ <
               static_cast<int>(client_.routines_order().size())) {

      // Select a static programmed routine.
      ::std::string routine_to_run = client_.routines_order()[current_routine_];
      programmed_routine_.LoadRoutineFromProto(
          client_.routines()[routine_to_run]);

      if (routine_to_run == "rotate") {
        current_runtime_ = 7;
      } else {
        current_runtime_ = 30;
      }

      // Don't run 420 routine on any other day.
      if (routine_to_run == "rasta") {
        continue;
      }

      ::std::cout << "Playing routine \"" << routine_to_run
                  << "\" with runtime " << current_runtime_ << ::std::endl;

      next_state = RUN_PROGRAMMED_ROUTINE;

      break;
    } else {
      current_routine_ -= client_.routines_order().size();
      dynamic_routines_[current_routine_]->Reset();
      next_state = RUN_DYNAMIC_ROUTINE;

      ::std::cout << "Playing dynamic routine \""
                  << dynamic_routines_[current_routine_]->name()
                  << "\" with runtime " << current_runtime_ << ::std::endl;

      break;
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
