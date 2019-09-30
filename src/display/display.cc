#include "display.h"

namespace illuminate {
namespace display {

Display::Display() :
// #ifdef RASPI_DEPLOYMENT
//     visualizer_(new LedStrip(kNumberOfLeds)),
// #else
//     visualizer_(new Simulator(kNumberOfLeds)),
// #endif
    phased_loop_(kFramesPerSecond),
    running_(false),
    last_iteration_(::std::numeric_limits<double>::infinity()),
    state_(STARTUP),
    current_routine_(-1),
    last_routine_(-1),
    programmed_routine_(kNumberOfLeds),
    current_runtime_(0) {

  dynamic_routines_.push_back(
      new routines::LineHighlightRoutine(kNumberOfLeds));
  dynamic_routines_.push_back(new routines::OutlineRoutine(kNumberOfLeds));
  dynamic_routines_.push_back(new routines::MovieTheaterRoutine(kNumberOfLeds));
  dynamic_routines_.push_back(new routines::TdxRoutine(kNumberOfLeds));
}

void Display::Run() {
  running_ = true;

  while (running_) {
    RunIteration();
    phased_loop_.SleepUntilNext();
  }
}

void Display::RunIteration() {
  // time_t theTime = time(NULL);
  // struct tm *aTime = localtime(&theTime);
  // int hour = aTime->tm_hour;
  // int day_of_month = aTime->tm_mday;
  // int month = aTime->tm_mon;
  // int day_of_week = aTime->tm_wday;
  // CheckFps();

  // if (!visualizer_->Render()) {
  //   Quit();
  // }

  // bool animation_complete = false;

  // // Dim the sign at later hours of the night.
  // visualizer_->set_brightness(GetBrightness(aTime));

  // switch (state_) {
  //   case STARTUP:
  //     for (int i = 0; i < kNumberOfLeds; i++) {
  //       visualizer_->SetLed(i, 0, 0, 0);
  //     }

  //     SetState(CONNECTING_TO_SERVER);
  //     break;

  //   case LED_OVERRIDE:
  //     static int current = 0;

  //     for (int i = 0; i < kNumberOfLeds; i++) {
  //       if (led_override_ == -1) {
  //         if (current == i) {
  //           visualizer_->SetLed(i, 0, 255, 0);
  //         } else {
  //           visualizer_->SetLed(i, 0, 0, 0);
  //         }
  //       } else if (i < led_override_) {
  //         visualizer_->SetLed(i, 10, 0, 0);
  //       } else if (i == led_override_) {
  //         visualizer_->SetLed(i, 255, 255, 255);
  //       } else {
  //         visualizer_->SetLed(i, 0, 0, 0);
  //       }
  //     }

  //     if (led_override_ == -1) {
  //       ::std::cout << current << ::std::endl;
  //       current = (current + 1) % 550;
  //     }

  //     break;

  //   case CONNECTING_TO_SERVER:
  //     for (int i = 0; i < kNumberOfLeds; i++) {
  //       visualizer_->SetLed(i, 0, 0, 100);
  //     }

  //     if (client_.connected()) {
  //       SetState(DOWNLOADING_ROUTINES);
  //     }

  //     break;

  //   case DOWNLOADING_ROUTINES:
  //     client_.FetchData();
  //     SetState(WAIT_FOR_DOWNLOAD_TO_COMPLETE);

  //     break;

  //   case WAIT_FOR_DOWNLOAD_TO_COMPLETE:
  //     for (int i = 0; i < kNumberOfLeds; i++) {
  //       visualizer_->SetLed(i, 0, 0, 255);
  //     }

  //     if (!client_.connected()) {
  //       SetState(CONNECTING_TO_SERVER);
  //     }

  //     if (client_.FetchFinished()) {
  //       visualizer_->SetPixelLayout(client_.pixel_layout());

  //       ::std::cout << "hour is " << hour << ::std::endl;
  //       ::std::cout << "day_of_week is " << day_of_week << ::std::endl;
  //       ::std::cout << "day_of_month is " << day_of_month << ::std::endl;
  //       ::std::cout << "month is " << month << ::std::endl;

  //       animation_complete = true;
  //     }

  //     break;

  //   case BLANK:
  //     for (int i = 0; i < kNumberOfLeds; i++) {
  //       visualizer_->SetLed(i, kBlankBrightness, kBlankBrightness,
  //                           kBlankBrightness);
  //     }

  //     break;

  //   case RUN_PROGRAMMED_ROUTINE:
  //     if (client_.routines_order().size() < 1) {
  //       SetState(BLANK);
  //     }

  //     programmed_routine_.DrawFrame(*visualizer_);

  //     if (programmed_routine_.AnimationComplete(current_runtime_)) {
  //       animation_complete = true;
  //     }

  //     break;

  //   case RUN_DYNAMIC_ROUTINE:
  //     routines::Routine *dynamic_routine =
  //     dynamic_routines_[current_routine_];
  //     dynamic_routine->DrawFrame(*visualizer_);

  //     if (dynamic_routine->AnimationComplete(current_runtime_)) {
  //       animation_complete = true;
  //     }

  //     break;
  // }

  // // Select the next state if the current animation completes.
  // while (animation_complete) {
  //   if (OverrideOnFourthOfJuly(aTime) || OverrideOnPride(aTime) ||
  //   OverrideOnWeekday(aTime) || OverrideOnThursday(aTime) ||
  //   OverrideOnSaturday(aTime)) {
  //     break;
  //   }

  //   int all_routines_count =
  //       client_.routines_order().size() + dynamic_routines_.size();

  //   current_routine_ = rand() % all_routines_count;

  //   // Don't repeat routines back-to-back.
  //   if (current_routine_ == last_routine_) {
  //     current_routine_ = (current_routine_ + 1) % all_routines_count;
  //   }

  //   last_routine_ = current_routine_;

  //   if (all_routines_count == 0) {
  //     SetState(BLANK);
  //     animation_complete = false;
  //   } else if (current_routine_ <
  //              static_cast<int>(client_.routines_order().size())) {

  //     // Select a static programmed routine.
  //     ::std::string routine_to_run =
  //     client_.routines_order()[current_routine_];
  //     programmed_routine_.LoadRoutineFromProto(
  //         client_.routines()[routine_to_run]);

  //     programmed_routine_.RandomizeFrame();

  //     current_runtime_ = GetAnimatedRuntime(routine_to_run);
  //     if (current_runtime_ == 0) {
  //       continue;
  //     }

  //     ::std::cout << "Playing routine \"" << routine_to_run
  //                 << "\" with runtime " << current_runtime_ << ::std::endl;

  //     SetState(RUN_PROGRAMMED_ROUTINE);
  //     break;
  //   } else {
  //     current_routine_ -= client_.routines_order().size();
  //     dynamic_routines_[current_routine_]->Reset();
  //     current_runtime_ =
  //         GetAnimatedRuntime(dynamic_routines_[current_routine_]->name());
  //     if (current_runtime_ == 0) {
  //       continue;
  //     }

  //     SetState(RUN_DYNAMIC_ROUTINE);

  //     ::std::cout << "Playing dynamic routine \""
  //                 << dynamic_routines_[current_routine_]->name()
  //                 << "\" with runtime " << current_runtime_ << ::std::endl;

  //     break;
  //   }
  // }
}

int Display::GetAnimatedRuntime(::std::string routine_to_run) {
  // Don't run static routines when doing animated ones.
  if (routine_to_run == "tdx_routine" || routine_to_run == "rasta") {
    return 0;
  }

  if (routine_to_run == "rotate" || routine_to_run == "rainbow_diagonal") {
    return 7;
  } else {
    return rand() % 30 + 30;
  }
}

// bool Display::OverrideOnThursday(struct tm *aTime) {
//   int hour = aTime->tm_hour;
//   int day_of_week = aTime->tm_wday;

//   if (!((day_of_week == 4 && hour > 12) || (day_of_week == 5 && hour <= 12)))
//   {
//     return false;
//   }

//   ::std::string found_routine = "";

//   int i = 0;
//   for (::std::string routine_name : client_.routines_order()) {
//     if (routine_name == "hues") {
//       found_routine = routine_name;
//       break;
//     }

//     i++;
//   }

//   if (found_routine == "") {
//     SetState(BLANK);
//   } else {
//     SetState(RUN_PROGRAMMED_ROUTINE);
//     current_runtime_ = 60;

//     programmed_routine_.LoadRoutineFromProto(client_.routines()[found_routine]);

//     current_routine_ = i + dynamic_routines_.size();
//     SetState(RUN_PROGRAMMED_ROUTINE);
//   }

//   return true;
// }

// bool Display::OverrideOnFourthOfJuly(struct tm *aTime) {
//   int hour = aTime->tm_hour;
//   int month = aTime->tm_mon;
//   int month_day = aTime->tm_mday;

//   if (!((month == 6 && month_day == 2 && hour > 12) || (month == 6 &&
//   month_day == 3 && hour <= 12))) {
//     return false;
//   }

//   ::std::string found_routine = "";

//   int i = 0;
//   for (::std::string routine_name : client_.routines_order()) {
//     if (routine_name == "american_flag") {
//       found_routine = routine_name;
//       break;
//     }

//     i++;
//   }

//   if (found_routine == "") {
//     SetState(BLANK);
//   } else {
//     SetState(RUN_PROGRAMMED_ROUTINE);
//     current_runtime_ = 60;

//     programmed_routine_.LoadRoutineFromProto(client_.routines()[found_routine]);

//     current_routine_ = i + dynamic_routines_.size();
//     SetState(RUN_PROGRAMMED_ROUTINE);
//   }

//   return true;
// }

// bool Display::OverrideOnPride(struct tm *aTime) {
//   int hour = aTime->tm_hour;
//   int month = aTime->tm_mon;
//   int month_day = aTime->tm_mday;

//   if (!((month == 5 && month_day == 28 && hour > 12) || (month == 5 &&
//   month_day == 29 && hour <= 12))) {
//     return false;
//   }

//   ::std::string found_routine = "";

//   int i = 0;
//   for (::std::string routine_name : client_.routines_order()) {
//     if (routine_name == "rainbow_diagonal") {
//       found_routine = routine_name;
//       break;
//     }

//     i++;
//   }

//   if (found_routine == "") {
//     SetState(BLANK);
//   } else {
//     SetState(RUN_PROGRAMMED_ROUTINE);
//     current_runtime_ = 60;

//     programmed_routine_.LoadRoutineFromProto(client_.routines()[found_routine]);

//     current_routine_ = i + dynamic_routines_.size();
//     SetState(RUN_PROGRAMMED_ROUTINE);
//   }

//   return true;
// }

// bool Display::OverrideOnSaturday(struct tm *aTime) {
//   int hour = aTime->tm_hour;
//   int day_of_week = aTime->tm_wday;

//   if (!((day_of_week == 6 && hour > 12) || (day_of_week == 0 && hour <= 12)))
//   {
//     return false;
//   }

//   ::std::string found_routine = "";

//   int i = 0;
//   for (::std::string routine_name : client_.routines_order()) {
//     if (routine_name == "projector_visuals") {
//       found_routine = routine_name;
//       break;
//     }

//     i++;
//   }

//   if (found_routine == "") {
//     SetState(BLANK);
//   } else {
//     SetState(RUN_PROGRAMMED_ROUTINE);
//     current_runtime_ = 60;

//     programmed_routine_.LoadRoutineFromProto(client_.routines()[found_routine]);

//     current_routine_ = i + dynamic_routines_.size();
//     SetState(RUN_PROGRAMMED_ROUTINE);
//   }

//   return true;
// }

// bool Display::OverrideOnWeekday(struct tm *aTime) {
//   int hour = aTime->tm_hour;
//   int day_of_week = aTime->tm_wday;

//   // Just show TDX light on any day but Friday and Saturday.
//   if (!((day_of_week < 4 && day_of_week > 1)
//       || (day_of_week == 4 && hour <= 12)
//       || (day_of_week == 1 && hour > 12)) && !(hour >= 2 && hour < 12)) {
//     return false;
//   }

//   ::std::string found_routine = "";

//   int i = 0;
//   for (::src::display::routines::Routine *routine : dynamic_routines_) {
//     if (routine->name() == "tdx_routine") {
//       found_routine = routine->name();
//       break;
//     }

//     i++;
//   }

//   if (found_routine == "") {
//     SetState(BLANK);
//   } else {
//     SetState(RUN_PROGRAMMED_ROUTINE);
//     current_runtime_ = 30;

//     current_routine_ = i;
//     dynamic_routines_[current_routine_]->Reset();
//     SetState(RUN_DYNAMIC_ROUTINE);
//   }

//   return true;
// }

double Display::GetBrightness(struct tm *aTime) {
  double hour = aTime->tm_hour + aTime->tm_min / 60.0 + aTime->tm_sec / 3600.0;

  // When the day increments wraps, add to the hour counter to compensate.
  if (hour < 10) {
    hour += 24;
  }

  double progress =
      (hour - kDimFadeStartHour) / (kDimFadeEndHour - kDimFadeStartHour);
  progress = ::std::min(::std::max(progress, 0.0), 1.0);

  return kMaxBrightness - (kMaxBrightness - kMinBrightness) * progress;
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

void Display::SetState(State state) { state_ = state; }

void Display::Quit() { running_ = false; }

} // namespace display
} // namespace illuminate
