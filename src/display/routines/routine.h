#pragma once

#include "src/display/visualizer/visualizer.h"

class Routine {
 public:
  Routine() {}

  virtual void DrawFrame(Visualizer &visualizer) = 0;
  virtual bool AnimationComplete() = 0;
};