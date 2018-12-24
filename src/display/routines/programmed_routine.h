#pragma once

#include "routine.h"

#include "src/messages.pb.h"

class ProgrammedRoutine : public Routine {
 public:
  ProgrammedRoutine() : routine_(nullptr), frame_(0) {}

  void DrawFrame(Visualizer &visualizer) {
    // ::std::cout << "Drawing frame " << frame_ << ::std::endl;
    if (routine_ == nullptr) {
      return;
    }

    ::src::Frame current_frame = routine_->frames(frame_);
    frame_ = (frame_ + 1) % routine_->frames_size();
    // ::std::cout << routine_->frames_size() << ::std::endl;

    for (int i = 0; i < current_frame.pixel_colors_size(); i++) {
      int32_t color = current_frame.pixel_colors(i);
      unsigned char r = color & 0xFF;
      unsigned char g = (color >> 8) & 0xFF;
      unsigned char b = (color >> 16) & 0xFF;

      visualizer.SetLed(i, r, g, b);
    }
  }

  bool AnimationComplete() {
    if (routine_ == nullptr) {
      return true;
    }

    return frame_ >= routine_->frames_size() - 2;
  }

  void LoadRoutineFromProto(::src::Routine &routine) {
    routine_ = &routine;
    frame_ = 0;
  }

 private:
  ::src::Routine *routine_;
  int frame_;
};