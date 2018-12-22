package(default_visibility = ['//visibility:public'])

cc_library(
  name = 'client',
  visibility = ['//visibility:public'],
  srcs = [
    'client.cc'
  ],
  hdrs = [
    'client.h'
  ],
  deps = [
    "@socketio_client_cpp//:socketio_client_cpp",
  ],
  copts = [
    '-std=c++11',
    '-pipe',
    '-Wno-unused-parameter',
    '-Wno-unused-private-field',
  ],
)
