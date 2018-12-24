#pragma once

#include <iostream>

#include "sio_client.h"
#include "sio_socket.h"

#include "src/messages.pb.h"
#include "lib/base64_tools/base64_tools.h"

namespace src {
namespace display {
namespace client {
namespace {
static constexpr double kReconnectDelay = 0.2;
} // namespace

class Client {
 public:
  Client(const char * server_url);

  void FetchData();

  ::src::PixelLayout &pixel_layout();
  bool connected();
  bool got_pixel_layout();

 private:
  ::sio::client client_;
  bool connected_;
  bool got_pixel_layout_;

  ::src::PixelLayout pixel_layout_;
};

} // namespace client
} // namespace display
} // namespace src
