#include "display.h"

// extern "C" {
// ws2811_return_t ws2811_init(ws2811_t *ws2811);
// }

// ws2811_led_t leds[LED_COUNT];

// ws2811_channel_t channel_0 = {GPIO_PIN, 0, LED_COUNT, STRIP_TYPE, leds, 255,
//                               0,        0, 0,         0,          nullptr};

// ws2811_channel_t channel_1 = {GPIO_PIN, 0, LED_COUNT, STRIP_TYPE, nullptr,
// 255,
//                               0,        0, 0,         0,          nullptr};

// ws2811_t ledstring = {0,           nullptr, nullptr,
//                       TARGET_FREQ, DMA,     {channel_0, channel_1}};

// struct Pixel {
//   int identity;
//   std::vector<unsigned char> r;
//   std::vector<unsigned char> g;
//   std::vector<unsigned char> b;
// };

// struct Routine {
//   int identity;
//   int cycles;
//   double interval;
//   std::vector<Pixel> pixels;
// };

// std::mutex routines_mutex;
// std::vector<Routine> routines, routines_buffer;
// sio::client client;
// bool play = true;
// bool reset = false;

// bool disable_lights = false;

// ws2811_led_t rgb_to_led_color(unsigned char red, unsigned char green,
//                               unsigned char blue) {
//   unsigned char white = 0;

//   return (white << 24) | (blue << 16) | (green << 8) | red;
// }

// void on_connect() {
//   std::cout << "CONNECTED!" << std::endl;

//   client.socket()->on(
//       "toggle lights sign",
//       sio::socket::event_listener_aux(
//           [&](std::string const &name, sio::message::ptr const &data,
//               bool isAck, sio::message::list &ack_resp) {
//             disable_lights = !disable_lights;
//           }));
// }

// void on_close(sio::client::close_reason const &reason) {
//   std::cout << "closed " << std::endl;
// }

// void on_fail() { std::cout << "failed " << std::endl; }

// char mix(char one, char two, float slept, float interval) {
//   float mix = slept / interval;
//   return one * (1 - mix) + two * (mix);
// }

// typedef struct {
//   double r; // a fraction between 0 and 1
//   double g; // a fraction between 0 and 1
//   double b; // a fraction between 0 and 1
// } rgb;

// typedef struct {
//   double h; // angle in degrees
//   double s; // a fraction between 0 and 1
//   double v; // a fraction between 0 and 1
// } hsv;

// static rgb hsv2rgb(hsv in);

// rgb hsv2rgb(hsv in) {
//   double hh, p, q, t, ff;
//   long i;
//   rgb out;

//   if (in.s <= 0.0) { // < is bogus, just shuts up warnings
//     out.r = in.v;
//     out.g = in.v;
//     out.b = in.v;
//     return out;
//   }
//   hh = in.h;
//   if (hh >= 360.0)
//     hh = 0.0;
//   hh /= 60.0;
//   i = (long)hh;
//   ff = hh - i;
//   p = in.v * (1.0 - in.s);
//   q = in.v * (1.0 - (in.s * ff));
//   t = in.v * (1.0 - (in.s * (1.0 - ff)));

//   switch (i) {
//   case 0:
//     out.r = in.v;
//     out.g = t;
//     out.b = p;
//     break;
//   case 1:
//     out.r = q;
//     out.g = in.v;
//     out.b = p;
//     break;
//   case 2:
//     out.r = p;
//     out.g = in.v;
//     out.b = t;
//     break;

//   case 3:
//     out.r = p;
//     out.g = q;
//     out.b = in.v;
//     break;
//   case 4:
//     out.r = t;
//     out.g = p;
//     out.b = in.v;
//     break;
//   case 5:
//   default:
//     out.r = in.v;
//     out.g = p;
//     out.b = q;
//     break;
//   }
//   return out;
// }

// class Blank {
//  public:
//   Blank(int num_leds) : num_leds_(num_leds) {}

//   void RunIteration(ws2811_t &leds) {
//     for (int i = 0; i < num_leds_; i++) {
//       leds.channel[0].leds[i] = rgb_to_led_color(0, 0, 0);
//     }
//   }

//  private:
//   int num_leds_;
// };

// double GetCurrentTime() {
//   return ::std::chrono::duration_cast<::std::chrono::nanoseconds>(
//              ::std::chrono::system_clock::now().time_since_epoch())
//              .count() *
//          1e-9;
// }

// void play_lights() {
//   std::cout << "PLAYING LIGHTS!" << std::endl;
//   ws2811_return_t ret;

//   // Initialize routine classes.
//   int selected_routine = rand() % 6;
//   Blank blank(LED_COUNT);

//   if ((ret = ws2811_init(&ledstring)) != WS2811_SUCCESS) {
//     fprintf(stderr, "ws2811_init failed\n");
//     return;
//   }

//   while (true) {
//     reset = false;

//     routines_mutex.lock();
//     std::vector<Routine> routines_tmp = routines;
//     routines_mutex.unlock();
//     //  const float brightness = 1.0;
//     double interval = 1 / 30.0;

//     double time = 0;

//     while (!reset && play) {
//       double start = GetCurrentTime();

//       switch (disable_lights ? -1 : selected_routine) {
//       case -1:
//         blank.RunIteration(ledstring);
//         break;
//       }

//       if (rand() % (1000000) < 100) {
//         selected_routine = rand() % 6;
//         rainbow.Reset();
//       }

//       if ((ret = ws2811_render(&ledstring)) != WS2811_SUCCESS) {
//         fprintf(stderr, "ws2811_render failed\n");
//         break;
//       }

//       ::std::cout << 1.0 / (GetCurrentTime() - time) << ::std::endl;
//       time = GetCurrentTime();
//       usleep((interval - GetCurrentTime() + start) * 1e6);
//     }
//   }

//   ::std::cout << "END\n";

//   ws2811_fini(&ledstring);
// }

// int main() {
//   std::thread lights_player(play_lights);

//   client.set_open_listener(on_connect);
//   client.set_close_listener(on_close);
//   client.set_fail_listener(on_fail);
//   client.connect("http://comran.org/");

//   lights_player.join();
// }

// NEW /////////////////////////////////////////////////////////////////////////
namespace src {
namespace display {

Display::Display() :
    phased_loop_(kFramesPerSecond),
    running_(false),
    last_iteration_(::std::numeric_limits<double>::infinity()) {}

void Display::Run() {
  running_ = true;

  while (running_) {
    RunIteration();
    phased_loop_.SleepUntilNext();
  }
}

void Display::RunIteration() {
  double current_time =
      ::std::chrono::duration_cast<::std::chrono::nanoseconds>(
          ::std::chrono::system_clock::now().time_since_epoch())
          .count() *
      1e-9;

  double current_fps =
      last_iteration_ == ::std::numeric_limits<double>::infinity()
          ? 0
          : 1.0 / (current_time - last_iteration_);

  ::std::cout << "Frame FPS: " << ::std::fixed << ::std::setprecision(1)
              << current_fps << ::std::endl;

  last_iteration_ = current_time;
}

void Display::Quit() {
  running_ = false;
}

} // namespace display
} // namespace src