// #include "client.h"

// namespace src {
// namespace display {
// namespace client {

// Client::Client(const char *server_url) :
//     connected_(false),
//     got_pixel_layout_(false),
//     got_all_routines_(false),
//     got_callback_(false) {
//   client_.set_open_listener([this]() {
//     ::std::cout << "Connect!\n";

//     connected_ = true;
//   });

//   client_.set_close_listener([this](::sio::client::close_reason const
//   &reason) {
//     ::std::cout << "Disconnected!\n";

//     (void)reason;
//     connected_ = false;
//   });

//   client_.set_reconnecting_listener([this]() {
//     ::std::cout << "Reconnecting!\n";

//     connected_ = false;
//   });

//   client_.set_reconnect_delay(kReconnectDelay * 1e3);
//   client_.connect(server_url);
// }

// void Client::FetchData() {
//   // Get pixel mapping.
//   client_.socket()->emit(
//       "get_pixel_locations", ::sio::string_message::create(""),
//       [&](::sio::message::list const &msg) {
//         ::std::string serialized_pixel_locations =
//             ::lib::base64_tools::Decode(msg[0].get()->get_string());
//         pixel_layout_.ParseFromString(serialized_pixel_locations);

//         got_pixel_layout_ = true;
//       });

//   // Download all routines.
//   client_.socket()->emit(
//       "get_routine_list", ::sio::string_message::create(""),
//       [&](::sio::message::list const &msg) {
//         ::std::vector<::std::string> routine_list;

//         for (size_t i = 0; i < msg[0].get()->get_map().size(); i++) {
//           ::std::string index_string = ::std::to_string(i);
//           routine_list.push_back(
//               msg[0].get()->get_map()[index_string].get()->get_string());
//         }

//         got_callback_ = true;
//         DownloadRoutines(routine_list);
//       });
// }

// bool Client::FetchFinished() {
//   if (!got_pixel_layout_) {
//     return false;
//   }

//   if (!got_callback_) {
//     return false;
//   }

//   for (size_t i = 0; i < routines_to_receive_.size(); i++) {
//     ::std::string routine_to_receive = routines_to_receive_[i];
//     if (partial_routines_sizes_[routine_to_receive] < 0) {
//       continue;
//     }

//     if (partial_routines_[routine_to_receive].size() <
//         static_cast<size_t>(partial_routines_sizes_[routine_to_receive])) {
//       continue;
//     }

//     ::std::string reassembled_data = "";
//     for (int j = 0; j < partial_routines_sizes_[routine_to_receive]; j++) {
//       reassembled_data =
//           reassembled_data + partial_routines_[routine_to_receive][j];
//     }

//     ::std::string decoded_data =
//     ::lib::base64_tools::Decode(reassembled_data);

//     ::src::Routine routine;
//     routine.ParseFromString(decoded_data);
//     ::std::cout << "Received " << routine.name() << " with "
//                 << routine.frames_size() << " frames" << ::std::endl;

//     routines_[routine.name()] = routine;
//     routines_to_receive_.erase(routines_to_receive_.begin() + i);
//     i--;
//   }

//   return routines_to_receive_.size() < 1;
// }

// void Client::DownloadRoutines(::std::vector<::std::string> routine_list) {
//   ::std::string identifier = "receive_routines_" + ::std::to_string(rand());

//   client_.socket()->on(
//       identifier,
//       sio::socket::event_listener_aux(
//           [&](std::string const &name, sio::message::ptr const &data,
//               bool isAck, sio::message::list &ack_resp) {
//             ::std::string routine_name =
//                 data.get()->get_map()["name"].get()->get_string();
//             int count = data.get()->get_map()["count"].get()->get_int();
//             partial_routines_[routine_name][count] =
//                 data.get()->get_map()["payload"].get()->get_string();
//           }));

//   // Send out requests for all routines.
//   routines_to_receive_.insert(routines_to_receive_.end(),
//   routine_list.begin(),
//                               routine_list.end());

//   routines_order_.insert(routines_order_.end(), routine_list.begin(),
//                          routine_list.end());

//   for (::std::string routine : routine_list) {
//     partial_routines_sizes_[routine] = -1;

//     ::sio::message::ptr request = ::sio::object_message::create();
//     request.get()->get_map()["name"] =
//     ::sio::string_message::create(routine);
//     request.get()->get_map()["rx_identifier"] =
//         ::sio::string_message::create(identifier);

//     ::sio::message::list msg;
//     msg.push(request);

//     client_.socket()->emit("get_partial_routine", msg);

//     client_.socket()->emit("get_routine_number_of_partial_routines",
//                            ::sio::string_message::create(routine),
//                            [this, routine](::sio::message::list const &msg) {
//                              partial_routines_sizes_[routine] =
//                                  msg[0].get()->get_int();
//                            });
//   }
// }

// ::src::PixelLayout &Client::pixel_layout() { return pixel_layout_; }
// ::std::vector<::std::string> &Client::routines_order() {
//   return routines_order_;
// }
// ::std::unordered_map<::std::string, ::src::Routine> &Client::routines() {
//   return routines_;
// }

// bool Client::connected() { return connected_; }

// } // namespace client
// } // namespace display
// } // namespace src
