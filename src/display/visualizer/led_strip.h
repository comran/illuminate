#pragma once

#include "ws2811.h"

#include <cmath>

#include "src/display/visualizer/visualizer.h"
#include "src/messages.pb.h"

namespace {
static const int kLedStripGpioPin = 10;
static const int kLedStripDma = 10;
} // namespace

class LedStrip : public Visualizer {
 public:
  LedStrip(int number_of_leds) :
      number_of_leds_(number_of_leds),
      brightness_(1) {
    ws2811_led_t leds[number_of_leds];

    ws2811_channel_t channel_0 = {
        kLedStripGpioPin, // GPIO number
        0,                // Invert output signal
        number_of_leds,   // Number of LEDs, 0 if channel is unused.
        WS2811_STRIP_GBR, // Strip color layout
        leds,             // LED buffer
        255,              // Brightness value
        0,                // White shift value
        0,                // Red shift value
        0,                // Green shift value
        0,                // Blue shift value
        nullptr           // Gamma correction
    };

    ws2811_channel_t channel_1 = {
        kLedStripGpioPin, // GPIO number
        0,                // Invert output signal
        0,                // Number of LEDs, 0 if channel is unused.
        WS2811_STRIP_GBR, // Strip color layout
        leds,             // LED buffer
        255,              // Brightness value
        0,                // White shift value
        0,                // Red shift value
        0,                // Green shift value
        0,                // Blue shift value
        nullptr           // Gamma correction
    };

    leds_ = {
        0,                     // Render wait time
        nullptr,               // Device
        nullptr,               // Raspi hardware information
        WS2811_TARGET_FREQ,    // Required output frequency
        kLedStripDma,          // DMA number
        {channel_0, channel_1} // Channels
    };

    ws2811_return_t ret = ws2811_init(&leds_);
    if (ret != WS2811_SUCCESS) {
      return;
    }
  }

  ~LedStrip() { ws2811_fini(&leds_); }

  bool Render() {
    ws2811_return_t ret = ws2811_render(&leds_);

    if (ret != WS2811_SUCCESS) {
      return false;
    }

    return true;
  }

  void SetLed(int led, unsigned char r, unsigned char g, unsigned char b) {
    if (led >= number_of_leds_) {
      return;
    }

    ws2811_led_t led_color = ((char)(b * brightness_) << 16) |
                             ((char)(g * brightness_) << 8) |
                             (char)(r * brightness_);

    leds_.channel[0].leds[led] = led_color;
  }

  void set_brightness(double brightness) {
    brightness_ = ::std::max(::std::min(brightness, 1.0), 0.0);
  }

  void SetPixelLayout(::src::PixelLayout &pixel_layout) { return; }

 private:
  ws2811_t leds_;
  int number_of_leds_;
  double brightness_;
};
