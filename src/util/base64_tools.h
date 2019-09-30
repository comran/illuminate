#pragma once

#include <string>
#include <thread>

namespace illuminate {
namespace util {

namespace {
const ::std::string kBase64Chars = //
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"   //
    "abcdefghijklmnopqrstuvwxyz"   //
    "0123456789+/";
} // namespace

::std::string Decode(::std::string const &encoded_string);
::std::string Encode(const unsigned char *src, size_t len);
::std::string Encode(::std::string str);
bool IsBase64(unsigned char c);

} // namespace util
} // namespace illuminate
