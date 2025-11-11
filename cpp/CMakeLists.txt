cmake_minimum_required(VERSION 3.20)
project(parity_arb_monitor LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

option(PARITY_ENABLE_SANITIZERS "Enable sanitizers for debug builds" OFF)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

add_library(parity_core
    src/feed_handler.cpp
    src/parity_engine.cpp
    src/ring_buffer.cpp
)

target_include_directories(parity_core
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_compile_options(parity_core
    PRIVATE
        -Wall -Wextra -Wpedantic
        $<$<CONFIG:Release>:-O3 -march=native -flto>
)

if(PARITY_ENABLE_SANITIZERS)
    target_compile_options(parity_core PRIVATE -fsanitize=address,undefined)
    target_link_options(parity_core PRIVATE -fsanitize=address,undefined)
endif()

add_executable(parity_daemon src/main.cpp)

target_link_libraries(parity_daemon PRIVATE parity_core)

