package(default_visibility = ['//visibility:public'])

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
    '//src/display/visualizer/led_strip:led_strip',
    '//lib/phased_loop:phased_loop',

    "@rpi_ws281x//:rpi_ws281x",
    "@socketio_client_cpp//:socketio_client_cpp",
  ],
  copts = [
    '-std=c++11',
    '-pipe',
    '-Wno-unused-parameter',
    '-Wno-unused-private-field',
  ],
)
