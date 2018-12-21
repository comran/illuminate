#pragma once

#include <cstdint>
#include <iostream>

#include "SDL.h"

#include "src/display/visualizer/visualizer.h"

namespace {
static int kDisplayWidth = 1280;
static int kDisplayHeight = 720;
} // namespace

class StdoutVisual : public Visualizer {
 public:
  StdoutVisual(int number_of_leds);
  ~StdoutVisual();

  bool Render();
  void SetLed(int led, unsigned char r, unsigned char g, unsigned char b);

 private:
  int number_of_leds_;
  uint32_t *leds_;

  SDL_Window *sdl_window_;
  SDL_Renderer *sdl_renderer_;
};