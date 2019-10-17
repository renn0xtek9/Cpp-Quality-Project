cmake_minimum_required(VERSION 3.0)

project(testcpp)

add_executable(testcpp main.cpp)

install(TARGETS testcpp RUNTIME DESTINATION bin)
