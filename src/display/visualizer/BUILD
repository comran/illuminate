package(default_visibility = ['//visibility:public'])

cc_library(
  name = 'visualizer',
  visibility = ['//visibility:public'],
  hdrs = [
    'visualizer.h'
  ],
)

cc_library(
  name = 'led_strip',
  visibility = ['//visibility:public'],
  srcs = [
    'led_strip.cc'
  ],
  hdrs = [
    'led_strip.h'
  ],
  deps = [
    ':visualizer',
    "@rpi_ws281x//:rpi_ws281x",
  ],
)

cc_library(
  name = 'stdout_visual',
  visibility = ['//visibility:public'],
  srcs = [
    'stdout_visual.cc'
  ],
  hdrs = [
    'stdout_visual.h'
  ],
  deps = [
    ':visualizer',
    '@SDL2//:SDL2'
  ],
)
