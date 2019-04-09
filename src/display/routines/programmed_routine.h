#pragma once

#include "routine.h"

#include <iostream>

#include "src/messages.pb.h"

namespace src {
namespace display {
namespace routines {

class ProgrammedRoutine : public Routine {
 public:
  ProgrammedRoutine(int number_of_leds) :
      Routine(number_of_leds),
      routine_(nullptr),
      frame_(0) {}

  void DrawFrame(Visualizer &visualizer) {
    if (routine_ == nullptr) {
      return;
    }

    ::src::Frame current_frame = routine_->frames(frame_);
    frame_ = (frame_ + 1) % routine_->frames_size();

    for (int i = 0; i < current_frame.pixel_colors_size(); i++) {
      int32_t color = current_frame.pixel_colors(i);
      unsigned char r = color & 0xFF;
      unsigned char g = (color >> 8) & 0xFF;
      unsigned char b = (color >> 16) & 0xFF;

      visualizer.SetLed(i, r, g, b);
    }
  }

  void LoadRoutineFromProto(::src::Routine &routine) {
    routine_ = &routine;
    frame_ = rand() % routine_->frames_size();
    Reset();
  }

  ::std::string name() { return routine_->name(); }

 private:
  ::src::Routine *routine_;
  int frame_;
};

} // namespace routines
} // namespace display
} // namespace src
