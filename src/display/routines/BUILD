package(default_visibility = ['//visibility:public'])

cc_library(
  name = 'routine',
  visibility = ['//visibility:public'],
  hdrs = [
    'routine.h'
  ],
  deps = [
    "//src/display/visualizer:visualizer",
  ],
)

cc_library(
  name = 'programmed_routine',
  visibility = ['//visibility:public'],
  hdrs = [
    'programmed_routine.h'
  ],
  deps = [
    ':routine',
    '//src:messages_cpp'
  ],
)
