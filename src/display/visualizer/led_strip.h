#pragma once

#include "ws2811.h"

#include "src/display/visualizer/visualizer.h"

namespace {
static const int kLedStripTargetFrequency = 800000;
static const int kLedStripGpioPin = 18;
static const int kLedStripDma = 5;
static const int kLedStripType = WS2811_STRIP_GBR;
} // namespace

class LedStrip : public Visualizer {
 public:
  LedStrip(int number_of_leds);
  ~LedStrip();

  bool Render();
  void SetLed(int led, unsigned char r, unsigned char g, unsigned char b);

 private:
  ws2811_t leds_;
};