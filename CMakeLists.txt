CMAKE_MINIMUM_REQUIRED (VERSION 3.0)
ENABLE_TESTING ()
SET (EXENAME testcpp)
PROJECT (${EXENAME} LANGUAGES CXX)
SET (CMAKE_CXX_STANDARD 14)
SET (CMAKE_CXX_EXTENSIONS OFF)
SET (CMAKE_CXX_STANDARD_REQUIRED ON)

LIST (APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake_modules/)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)

#include(${CMAKE_SOURCE_DIR}/cmake_modules/conanbuildinfo.cmake)
conan_basic_setup(PROFILE ${CMAKE_SOURCE_DIR}/conan_profiles/linux-x86)

# conan_basic_setup(TARGETS)
# conan_cmake_run(BASIC_SETUP)
#conan_cmake_install(
#  CONANFILE conanfile.txt
#  OPTIONS build_tests=False
#  INSTALL_ARGS -pr=${CMAKE_SOURCE_DIR}/conan_profiles/linux-x86 -s build_type=${CMAKE_BUILD_TYPE}
#  BUILD missing
#)

INCLUDE (CMakeListsFormatting)
INCLUDE (FormatEverything)
# INCLUDE (GenerateGitHashAtConfigTime)
INCLUDE (GenerateGitHashAtBuildTime)

ADD_SUBDIRECTORY (probelibrary)

ADD_SUBDIRECTORY (test)
ADD_EXECUTABLE (${EXENAME} main.cpp)
TARGET_INCLUDE_DIRECTORIES (${EXENAME} PRIVATE ${CMAKE_BINARY_DIR})
TARGET_LINK_LIBRARIES (${EXENAME} PUBLIC probe)

INSTALL (TARGETS ${EXENAME} RUNTIME DESTINATION bin)

ADD_CUSTOM_TARGET (
  disassemble
  COMMAND /usr/bin/objdump -S $<TARGET_FILE:testcpp> >
          ${CMAKE_BINARY_DIR}/${EXENAME}.dump
  DEPENDS ${EXENAME})

ADD_CUSTOM_TARGET (convert_to_assembly COMMAND g++ -S
                                               ${CMAKE_SOURCE_DIR}/main.cpp)
ADD_CUSTOM_TARGET (benchmark COMMAND $<TARGET_FILE:probe_benchmark> >
                                     ${CMAKE_SOURCE_DIR}/benchmark_report.txt)

ADD_DEPENDENCIES (${EXENAME} format)

ADD_SUBDIRECTORY (documentation)
