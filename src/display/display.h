#include "sio_client.h"
#include "sio_socket.h"

#include <unistd.h>

#include <algorithm>
#include <condition_variable>
#include <functional>
#include <iomanip>
#include <iostream>
#include <memory>
#include <mutex>
#include <string>
#include <thread>

#include "clk.h"
#include "dma.h"
#include "gpio.h"
#include "pwm.h"
#include "version.h"

#include <atomic>
#include <chrono>
#include <cmath>
#include <iostream>
#include <limits>

// #include "ws2811.h"

#include "lib/phased_loop/phased_loop.h"

#define TARGET_FREQ 800000
#define GPIO_PIN 18
#define DMA 5
#define STRIP_TYPE WS2811_STRIP_GBR
#define LED_COUNT 300

namespace src {
namespace display {
namespace {
constexpr int kFramesPerSecond = 30;
constexpr int kNumberOfLeds = 300;
} // namespace

class Display {
 public:
  Display();

  void Run();
  void RunIteration();
  void Quit();

 private:
  ::lib::phased_loop::PhasedLoop phased_loop_;
  ::std::atomic<bool> running_;

  double last_iteration_;
};

} // namespace display
} // namespace src
