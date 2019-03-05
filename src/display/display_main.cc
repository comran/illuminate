#include "display.h"

#include <stdlib.h>

int main(int argc, char **argv) {
  int led_override = -2;
  if (argc > 1) {
    led_override = atoi(argv[1]);
  }

  ::src::display::Display display(led_override);
  display.Run();
}
