#pragma once

#include <chrono>
#include <thread>

namespace illuminate {

class PhasedLoop {
 public:
  PhasedLoop(double frequency);
  void SleepUntilNext();

 private:
  double GetCurrentTime();

  double frequency_;
  double next_iteration_;
};

}
