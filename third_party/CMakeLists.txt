macro(find_or_build _package_name)
    cmake_parse_arguments(_fob "" "FIND_VARIABLE;INSTALL_SUFFIX" "CONFIGURE_ARGS" ${ARGN})
    if (NOT _fob_FIND_VARIABLE)
        set(_fob_FIND_VARIABLE "${_package_name}_ROOT")
    endif()
    if (NOT _fob_INSTALL_SUFFIX)
        set(_fob_INSTALL_SUFFIX "install")
    endif()
    set(_find_package_args ${_fob_UNPARSED_ARGUMENTS})
    if(${_package_name}_FOUND)
        message(WARNING "Package ${_package_name} already found")
    endif()

    if (NOT USE_SYSTEM_DEPENDENCIES OR TRUE)
        find_package(${_package_name} QUIET PATHS ${${_fob_FIND_VARIABLE}} NO_DEFAULT_PATH ${_find_package_args})
        if(${_package_name}_FOUND)
            message(STATUS "Found prebuilt ${_package_name} with version ${${_package_name}_VERSION}")
        else()
            find_package(${_package_name} QUIET ${_find_package_args})
            if(${_package_name}_FOUND)
                message(STATUS "Found prebuild ${_package_name} with version ${${_package_name}_VERSION}")
            endif()
        endif()
    endif()

    if(NOT ${_package_name}_FOUND)
        if(NOT BUILD_DEPENDENCIES)
            message(FATAL_ERROR "Could not find package ${_package_name}, and not allowed to build")
            return()
        endif()
        message(STATUS "Could not find package ${_package_name}, building instead")
        set(_build_script Build${_package_name}.cmake)
        set(_build_dir "${CMAKE_BINARY_DIR}/Build${_package_name}")
        configure_file(${CMAKE_CURRENT_LIST_DIR}/${_build_script}.in "${_build_dir}/CMakeLists.txt" @ONLY)

        execute_process(COMMAND ${CMAKE_COMMAND} -G "${CMAKE_GENERATOR}" ${_fob_CONFIGURE_ARGS} .
            RESULT_VARIABLE _configure_result
            WORKING_DIRECTORY ${_build_dir})
        if(_configure_result)
            message(FATAL_ERROR "CMake configuration step for package ${_package_name} failed: ${_configure_result}")
        endif()

        execute_process(COMMAND ${CMAKE_COMMAND} --build .
            RESULT_VARIABLE _build_result
            WORKING_DIRECTORY ${_build_dir})
        if(_build_result)
            message(FATAL_ERROR "Build step for package ${_package_name} failed: ${_build_result}")
        endif()

        set(${_fob_FIND_VARIABLE} "${_build_dir}/${_fob_INSTALL_SUFFIX}" CACHE STRING "Location of built ${_package_name}" FORCE)
        message(TRACE "Set ${_fob_FIND_VARIABLE}=${${_fob_FIND_VARIABLE}}")
        find_package(${_package_name} REQUIRED PATHS ${${_fob_FIND_VARIABLE}} NO_DEFAULT_PATH ${_find_package_args})
    else()
    endif()
endmacro()

################################################################################
# googletest ###################################################################
################################################################################
find_or_build(GTest)

################################################################################
# libzmq #######################################################################
################################################################################
find_or_build(ZeroMQ)

################################################################################
# cppzmq #######################################################################
################################################################################
find_or_build(cppzmq CONFIGURE_ARGS -D ZeroMQ_DIR=${ZeroMQ_DIR})

################################################################################
# protobuf #####################################################################
################################################################################
set(protobuf_MODULE_COMPATIBLE ON CACHE BOOL "" FORCE)
find_or_build(Protobuf)

# BUILD_DIR specifies the cpp_out parameter of protoc
# BUILD_PREFIX is the directory prefix for files built (this happens because of the --proto_path option)
function(add_protobuf_cpp_target _target_name)
    cmake_parse_arguments(_UBPC "" "BUILD_DIR;BUILD_PREFIX" "PROTOC_FLAGS" ${ARGN})
    if(NOT _UBPC_BUILD_DIR)
        set(_UBPC_BUILD_DIR "${CMAKE_CURRENT_BINARY_DIR}")
    endif()
    set(_proto_srcs "")
    set(_proto_hdrs "")
    foreach(_proto_file IN LISTS _UBPC_UNPARSED_ARGUMENTS)
        get_filename_component(_proto_dir "${_proto_file}" DIRECTORY)
        get_filename_component(_proto_path "${_proto_file}" ABSOLUTE BASE_DIR "${CMAKE_CURRENT_SOURCE_DIR}")
        get_filename_component(_proto_name "${_proto_file}" NAME_WE)
        set(_proto_hdr "${_UBPC_BUILD_DIR}/${_UBPC_BUILD_PREFIX}/${_proto_name}.pb.h")
        set(_proto_src "${_UBPC_BUILD_DIR}/${_UBPC_BUILD_PREFIX}/${_proto_name}.pb.cc")
        list(APPEND _proto_hdrs "${_proto_src}")
        list(APPEND _proto_srcs "${_proto_src}")

        add_custom_command(
            OUTPUT "${_proto_hdr}" "${_proto_src}"
            COMMENT "Running C++ protoc on ${_proto_file}"
            COMMAND protobuf::protoc
                    "--cpp_out=${_UBPC_BUILD_DIR}"
                    ${_UBPC_PROTOC_FLAGS}
                    ${_proto_path}
            WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
            DEPENDS ${_proto_path} protobuf::protoc
            VERBATIM
        )
    endforeach()
    if (${CMAKE_VERSION} VERSION_LESS "3.12.0")
        set(_lib_type STATIC)
    else()
        set(_lib_type OBJECT)
    endif()
    add_library("${_target_name}" STATIC ${_proto_srcs} ${_proto_hdrs})
    target_compile_options("${_target_name}" PRIVATE -Wno-unused-parameter)
    target_include_directories("${_target_name}" PUBLIC ${_UBPC_BUILD_DIR})
    target_link_libraries("${_target_name}" PUBLIC protobuf::libprotobuf)
endfunction()

################################################################################
# eigen ########################################################################
################################################################################
find_or_build(Eigen3)
