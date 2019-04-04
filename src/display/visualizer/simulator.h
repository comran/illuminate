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
  Simulator(int number_of_leds) :
      number_of_leds_(number_of_leds),
      leds_(new uint32_t[number_of_leds]),
      sdl_window_(nullptr),
      sdl_renderer_(nullptr),
      window_width_(0),
      window_height_(0),
      pixel_layout_(nullptr) {

    if (SDL_Init(SDL_INIT_EVERYTHING)) {
      ::std::cout << "init failed: " << SDL_GetError() << "\n";
      return;
    }
  }

  ~Simulator() {
    delete[] leds_;

    if (sdl_renderer_ != nullptr) {
      SDL_DestroyRenderer(sdl_renderer_);
      sdl_renderer_ = nullptr;
    }

    if (sdl_window_ != nullptr) {
      SDL_DestroyWindow(sdl_window_);
      sdl_window_ = nullptr;
    }

    SDL_Quit();
  }

  bool Render() {
    SDL_Event event;
    if (SDL_PollEvent(&event)) {
      switch (event.type) {
        case SDL_QUIT:
          return false;
      }
    }

    if (sdl_window_ == nullptr || sdl_renderer_ == nullptr) {
      return true;
    }

    SDL_SetRenderDrawColor(sdl_renderer_, 0, 0, 0, SDL_ALPHA_OPAQUE);
    SDL_RenderClear(sdl_renderer_);

    // Draw pixels.
    int kPixelSize = 15;

    for (int i = 0; i < number_of_leds_; i++) {
      SDL_Rect led;
      led.w = kPixelSize;
      led.h = kPixelSize;
      led.x = 200 + ::std::floor(((kPixelSize + 1) * i) % 300);
      led.y = 100 + ::std::floor((kPixelSize + 1) * i / 300) * (1 + kPixelSize);

      if (pixel_layout_ != nullptr &&
          i < pixel_layout_->pixel_locations_size()) {
        led.x = pixel_layout_->pixel_locations(i).x() * window_width_;
        led.y = pixel_layout_->pixel_locations(i).y() * window_height_;
      }

      int color = leds_[i];
      int r = color & 0xFF;
      int g = (color >> 8) & 0xFF;
      int b = (color >> 16) & 0xFF;

      SDL_SetRenderDrawColor(sdl_renderer_, r, g, b, SDL_ALPHA_OPAQUE);
      SDL_RenderFillRect(sdl_renderer_, &led);
    }

    SDL_RenderPresent(sdl_renderer_);

    return true;
  }

  void SetLed(int led, unsigned char r, unsigned char g, unsigned char b) {
    if (led >= number_of_leds_) {
      return;
    }

    uint32_t led_color = (b << 16) | (g << 8) | r;
    leds_[led] = led_color;
  }

  void SetPixelLayout(::src::PixelLayout &pixel_layout) {
    // Destroy old window.
    if (sdl_renderer_ != nullptr) {
      SDL_DestroyRenderer(sdl_renderer_);
    }

    if (sdl_window_ != nullptr) {
      SDL_DestroyWindow(sdl_window_);
    }

    window_width_ = kMaxWindowSize * pixel_layout.width();
    window_height_ = kMaxWindowSize * pixel_layout.height();

    if (SDL_CreateWindowAndRenderer(window_width_, window_height_,
                                    SDL_WINDOW_SHOWN, &sdl_window_,
                                    &sdl_renderer_)) {

      ::std::cout << "window open failed!\n";
      return;
    }

    SDL_SetWindowTitle(sdl_window_, "Illuminate");

    pixel_layout_ = &pixel_layout;
  }

 private:
  int number_of_leds_;
  uint32_t *leds_;

  SDL_Window *sdl_window_;
  SDL_Renderer *sdl_renderer_;

  int window_width_;
  int window_height_;

  ::src::PixelLayout *pixel_layout_;
};
