#include "stdout_visual.h"

StdoutVisual::StdoutVisual(int number_of_leds) :
    number_of_leds_(number_of_leds),
    leds_(new uint32_t[number_of_leds]),
    sdl_window_(nullptr),
    sdl_renderer_(nullptr) {

  if (SDL_Init(SDL_INIT_EVERYTHING)) {
    ::std::cout << "init failed: " << SDL_GetError() << "\n";
    return;
  }

  if (SDL_CreateWindowAndRenderer(kDisplayWidth, kDisplayHeight,
                                  SDL_WINDOW_SHOWN, &sdl_window_,
                                  &sdl_renderer_)) {
    ::std::cout << "window open failed!\n";
    return;
  }

  SDL_SetWindowTitle(sdl_window_, "Illuminate");
}

StdoutVisual::~StdoutVisual() {
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

void StdoutVisual::SetLed(int led, unsigned char r, unsigned char g,
                          unsigned char b) {

  uint32_t led_color = (b << 16) | (g << 8) | r;

  leds_[led] = led_color;
}

bool StdoutVisual::Render() {
  SDL_Event event;
  if (SDL_PollEvent(&event)) {
    switch (event.type) {
      case SDL_QUIT:
        return false;
    }
  }

  SDL_SetRenderDrawColor(sdl_renderer_, 0, 0, 0, SDL_ALPHA_OPAQUE);
  SDL_RenderClear(sdl_renderer_);

  // Draw pixels.
  int kPixelSize = 15;

  for (int i = 0; i < number_of_leds_; i++) {
    SDL_Rect led;
    led.w = kPixelSize;
    led.h = kPixelSize;
    led.x = 200 + (kPixelSize * i) % 300;
    led.y = 100 + ::std::floor(kPixelSize * i / 300) * kPixelSize;

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
