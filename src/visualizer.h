#pragma once

#include "messages.pb.h"

class Visualizer {
 public:
  Visualizer() {}
  virtual ~Visualizer() {}

  virtual bool Render() = 0;

  void SetLed(int led, int hex) {
    unsigned char r = (hex >> 16) & 0xFF;
    unsigned char g = (hex >> 8) & 0xFF;
    unsigned char b = (hex >> 0) & 0xFF;

    SetLed(led, r, g, b);
  }

  virtual void SetLed(int led, unsigned char r, unsigned char g,
                      unsigned char b) = 0;

  virtual void set_brightness(double brightness) = 0;

  virtual void SetPixelLayout(::src::PixelLayout &pixel_layout) = 0;
};
