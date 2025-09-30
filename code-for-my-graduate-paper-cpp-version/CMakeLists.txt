cmake_minimum_required(VERSION 3.10)
project(ISDIP_CPP)

set(CMAKE_CXX_STANDARD 17)

find_package(OpenCV REQUIRED)

include_directories(${OpenCV_INCLUDE_DIRS})
include_directories(include)

file(GLOB_RECURSE SOURCES "src/*.cpp")

add_executable(isdip_demo ${SOURCES})

target_link_libraries(isdip_demo ${OpenCV_LIBS})

if(WIN32)
    set_target_properties(isdip_demo PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    )
endif()