#pragma once

#include "src/messages.pb.h"

class Visualizer {
 public:
  Visualizer() {}
  virtual ~Visualizer() {}

  virtual bool Render() = 0;
  virtual void SetLed(int led, unsigned char r, unsigned char g,
                      unsigned char b) = 0;
  virtual void SetPixelLayout(::src::PixelLayout &pixel_layout) = 0;
};