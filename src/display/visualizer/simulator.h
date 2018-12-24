#pragma once

#include <cmath>
#include <cstdint>
#include <iostream>

#include "SDL.h"

#include "src/display/visualizer/visualizer.h"
#include "src/messages.pb.h"

namespace {
static int kMaxWindowSize = 1920;
} // namespace

class Simulator : public Visualizer {
 public:
  Simulator(int number_of_leds);
  ~Simulator();

  bool Render();
  void SetLed(int led, unsigned char r, unsigned char g, unsigned char b);
  void SetPixelLayout(::src::PixelLayout &pixel_layout);

 private:
  int number_of_leds_;
  uint32_t *leds_;

  SDL_Window *sdl_window_;
  SDL_Renderer *sdl_renderer_;

  int window_width_;
  int window_height_;

  ::src::PixelLayout *pixel_layout_;
};