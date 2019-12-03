cmake_minimum_required(VERSION 3.0)
enable_testing()
project(testcpp LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(OpenCV REQUIRED)
set(OpenCV_DIR "/usr/include/opencv")
include_directories(${OpenCV_INCLUDE_DIRS})

add_subdirectory(test)

add_executable(testcpp main.cpp)
target_link_libraries(testcpp ${OpenCV_LIBS})

install(TARGETS testcpp RUNTIME DESTINATION bin)
