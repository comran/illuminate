#pragma once

#include <queue>
#include <string>

#include "routines/routine.h"

namespace illuminate {
namespace scheduler {

class Scheduler {
 public:
  /**
   * Constructor
   */
  Scheduler();

  /**
   * Schedule a routine to be played.
   */
  void Add(routines::Routine *routine);

 private:
  ::std::queue<routines::Routine *> schedule_;
};

} // namespace scheduler
} // namespace illuminate
