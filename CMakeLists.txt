CMAKE_MINIMUM_REQUIRED (VERSION 3.0)
ENABLE_TESTING ()
SET (EXENAME testcpp)
PROJECT (${EXENAME} LANGUAGES CXX)
SET (CMAKE_CXX_STANDARD 14)
SET (CMAKE_CXX_EXTENSIONS OFF)
SET (CMAKE_CXX_STANDARD_REQUIRED ON)

LIST (APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake_modules/)
# INCLUDE (FindAllCppFiles)
INCLUDE (CMakeListsFormatting)
INCLUDE (format_everything)

ADD_SUBDIRECTORY (probelibrary)

ADD_SUBDIRECTORY (test)
ADD_EXECUTABLE (${EXENAME} main.cpp)
TARGET_LINK_LIBRARIES (${EXENAME} PUBLIC wtf)

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
