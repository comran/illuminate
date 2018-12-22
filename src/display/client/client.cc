#include "client.h"

namespace src {
namespace display {
namespace client {

Client::Client(const char * server_url) {
  client_.set_open_listener([this]() {
    ::std::cout << "Connect!\n";

    connected_ = true;

    client_.socket()->on(
        "toggle lights sign",
        ::sio::socket::event_listener_aux(
            [&](std::string const &name, sio::message::ptr const &data,
                bool isAck, sio::message::list &ack_resp) {
            }));
  });

  client_.set_close_listener([this](::sio::client::close_reason const &reason) {
    ::std::cout << "Disconnected!\n";

    (void) reason;

    connected_ = false;
  });

  client_.connect(server_url);
}

bool Client::connected() {
  return connected_;
}

} // namespace client
} // namespace display
} // namespace src