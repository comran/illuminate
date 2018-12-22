#pragma once

#include <iostream>

#include "sio_client.h"
#include "sio_socket.h"

namespace src {
namespace display {
namespace client {

class Client {
 public:
  Client(const char * server_url);

  bool connected();

 private:
  ::sio::client client_;
  bool connected_;
};

} // namespace client
} // namespace display
} // namespace src
