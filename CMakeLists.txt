cmake_minimum_required(VERSION 3.0)

list(APPEND CMAKE_MODULE_PATH
     ${CMAKE_CURRENT_SOURCE_DIR}/project/cmake_modules/)
include(CMakeListsFormatting)

enable_testing()
add_subdirectory(project)
add_subdirectory(workflow_test)
