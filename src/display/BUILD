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
    '//lib/phased_loop:phased_loop',

    "@rpi_ws281x//:rpi_ws281x",
  ] + cpu_select({
    'amd64': [
      '//src/display/visualizer:stdout_visual',
    ],
    'raspi': [
      '//src/display/visualizer:led_strip',
    ],
  }),
  copts = [
    '-std=c++11',
    '-pipe',
    '-Wno-unused-parameter',
    '-Wno-unused-private-field',
  ],
)
