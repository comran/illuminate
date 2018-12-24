package(default_visibility = ['//visibility:public'])

load('//tools/build_rules:select.bzl', 'cpu_select')

cc_binary(
  name = 'display',
  visibility = ['//visibility:public'],
  srcs = [
    'display_main.cc',
  ],
  deps = [
    ":display_lib"
  ],
)

cc_library(
  name = 'display_lib',
  visibility = ['//visibility:public'],
  srcs = [
    'display.cc'
  ],
  hdrs = [
    'display.h'
  ],
  deps = [
    '//src/display/client:client',
    '//src/display/routines:programmed_routine',
    '//lib/phased_loop:phased_loop',

    "@rpi_ws281x//:rpi_ws281x",
  ] + cpu_select({
    'amd64': [
      '//src/display/visualizer:simulator',
    ],
    'raspi': [
      '//src/display/visualizer:led_strip',
    ],
  }),
)
