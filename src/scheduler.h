#pragma once

#include <string>
#include <queue>

#include "routine.h"

namespace illuminate {

class Scheduler {
 public:
  /**
   * Constructor
   */
  Scheduler();

  /**
   * Schedule a routine to be played.
   */
  void Add(Routine *routine);

 private:
  ::std::queue<Routine *> schedule_;
};

}
