################################################################################
# CMake Config #################################################################
################################################################################
cmake_minimum_required(VERSION 3.5)
set(CMAKE_CXX_STANDARD 11)
project(illuminate)

if(POLICY CMP0074)
    cmake_policy(SET CMP0074 NEW)
endif()
cmake_policy(SET CMP0058 NEW)

################################################################################
# Options and cache variables ##################################################
################################################################################
option(USE_CCACHE "Use ccache if available" ON)
option(USE_STATIC_ANALYSIS "Use static analysis tools if available" OFF)
option(USE_ADDRESS_SANITIZER "Use ASAN if available" OFF)
option(USE_SYSTEM_DEPENDENCIES "Use dependencies installed in system (found by find_package)" ON)
option(BUILD_DEPENDENCIES "Build dependencies if not found in system" ON)

################################################################################
# Source Code ##################################################################
################################################################################
include(third_party/CMakeLists.txt)

add_protobuf_cpp_target(illuminate_proto src/proto/messages.proto
    BUILD_PREFIX "src/proto"
    PROTOC_FLAGS --proto_path "${CMAKE_SOURCE_DIR}")


file(GLOB_RECURSE ${PROJECT_NAME}_SRCS
	"src/*.cc")
file(GLOB_RECURSE ${PROJECT_NAME}_HDRS
    "src/*.h")

add_executable(${PROJECT_NAME} ${${PROJECT_NAME}_SRCS})
target_link_libraries(${PROJECT_NAME} PUBLIC illuminate_proto ${SDL2_LIBRARIES})
target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_BINARY_DIR}/src)
target_include_directories(${PROJECT_NAME} PUBLIC src)

