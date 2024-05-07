SET (EXENAME testcpp)
PROJECT (${EXENAME} LANGUAGES CXX)
SET (CMAKE_CXX_STANDARD 14)
SET (CMAKE_CXX_EXTENSIONS OFF)
SET (CMAKE_CXX_STANDARD_REQUIRED ON)

ADD_SUBDIRECTORY (probelibrary)

ADD_EXECUTABLE (${EXENAME} main.cpp)
TARGET_INCLUDE_DIRECTORIES (${EXENAME} PRIVATE ${CMAKE_BINARY_DIR})
TARGET_LINK_LIBRARIES (${EXENAME} PUBLIC probe)

INSTALL (TARGETS ${EXENAME} RUNTIME DESTINATION bin)

ADD_CUSTOM_TARGET (
  disassemble
  COMMAND /usr/bin/objdump -S $<TARGET_FILE:testcpp> >
          ${CMAKE_BINARY_DIR}/${EXENAME}.dump
  COMMENT "Disassemble ${EXENAME}"
  DEPENDS ${EXENAME})

ADD_CUSTOM_TARGET (
  convert_to_assembly
  COMMAND g++ -S
  COMMENT "Convert ${EXENAME} to assembly"
  ${CMAKE_SOURCE_DIR}/main.cpp)

ADD_CUSTOM_TARGET (
  benchmark
  COMMENT "Benchmark target"
  COMMAND $<TARGET_FILE:probe_benchmark> >
          ${CMAKE_SOURCE_DIR}/benchmark_report.txt)

ADD_TEST (
  NAME code_coverage
  COMMAND gcovr -r .. --fail-under-line 1.0 --html --html-details -o index.html
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR})
SET_TESTS_PROPERTIES (code_coverage PROPERTIES FIXTURES_CLEANUP unit_tests)

ADD_TEST (
  NAME benchmarking
  COMMAND $<TARGET_FILE:probe_benchmark>
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR})
SET_TESTS_PROPERTIES (benchmarking PROPERTIES DEPENDS benchmark)
