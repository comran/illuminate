// #pragma once

// #include <iostream>
// #include <map>
// #include <stdlib.h>
// #include <unordered_map>
// #include <vector>

// #include "sio_client.h"
// #include "sio_socket.h"

// #include "lib/base64_tools/base64_tools.h"
// #include "src/messages.pb.h"

// namespace src {
// namespace display {
// namespace client {
// namespace {
// static constexpr double kReconnectDelay = 0.2;
// } // namespace

// class Client {
//  public:
//   Client(const char *server_url);

//   void FetchData();
//   bool FetchFinished();

//   ::src::PixelLayout &pixel_layout();
//   ::std::vector<::std::string> &routines_order();
//   ::std::unordered_map<::std::string, ::src::Routine> &routines();
//   bool connected();

//  private:
//   void DownloadRoutines(::std::vector<::std::string> routine_list);

//   ::sio::client client_;
//   bool connected_;
//   bool got_pixel_layout_;
//   bool got_all_routines_;

//   bool got_callback_;
//   ::std::vector<::std::string> routines_to_receive_;
//   ::std::vector<::std::string> routines_order_;
//   ::std::unordered_map<::std::string, ::src::Routine> routines_;
//   ::std::unordered_map<::std::string, ::std::unordered_map<int,
//   ::std::string>>
//       partial_routines_;
//   ::std::unordered_map<::std::string, int> partial_routines_sizes_;

//   ::src::PixelLayout pixel_layout_;
// };

// } // namespace client
// } // namespace display
// } // namespace src
