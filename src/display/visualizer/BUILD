package(default_visibility = ['//visibility:public'])

cc_library(
  name = 'visualizer',
  visibility = ['//visibility:public'],
  hdrs = [
    'visualizer.h'
  ],
  deps = [
    "//src:messages_cpp",
  ],
)

cc_library(
  name = 'led_strip',
  visibility = ['//visibility:public'],
  hdrs = [
    'led_strip.h'
  ],
  deps = [
    ':visualizer',
    "@rpi_ws281x//:rpi_ws281x",
  ],
)

cc_library(
  name = 'simulator',
  visibility = ['//visibility:public'],
  hdrs = [
    'simulator.h'
  ],
  deps = [
    ':visualizer',
    '@SDL2//:SDL2'
  ],
)
