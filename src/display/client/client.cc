#include "client.h"

namespace src {
namespace display {
namespace client {

Client::Client(const char * server_url) : connected_(false), got_pixel_layout_(false) {
  client_.set_open_listener([this]() {
    ::std::cout << "Connect!\n";

    connected_ = true;

    // client_.socket()->on(
    //     "toggle lights sign",
    //     ::sio::socket::event_listener_aux(
    //         [&](std::string const &name, sio::message::ptr const &data,
    //             bool isAck, sio::message::list &ack_resp) {
    //         }));
  });

  client_.set_close_listener([this](::sio::client::close_reason const &reason) {
    ::std::cout << "Disconnected!\n";

    (void) reason;

    connected_ = false;
  });

  client_.set_reconnecting_listener([this]() {
    ::std::cout << "Reconnecting!\n";

    connected_ = false;
  });

  client_.set_reconnect_delay(kReconnectDelay * 1e3);

  client_.connect(server_url);
}

void Client::FetchData() {
  client_.socket()->emit("get_pixel_locations",
    ::sio::string_message::create(""),
    [&](::sio::message::list const& msg) {

    ::std::string serialized_pixel_locations = ::lib::base64_tools::Decode(msg[0].get()->get_string());
    pixel_layout_.ParseFromString(serialized_pixel_locations);

    got_pixel_layout_ = true;
  });
}

::src::PixelLayout& Client::pixel_layout() {
  return pixel_layout_;
}

bool Client::connected() {
  return connected_;
}

bool Client::got_pixel_layout() {
  return got_pixel_layout_;
}

} // namespace client
} // namespace display
} // namespace src