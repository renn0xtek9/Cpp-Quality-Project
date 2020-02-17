SET (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14 -pthread")
FIND_PACKAGE (GTest REQUIRED)
INCLUDE_DIRECTORIES (${GTEST_INCLUDE_DIRS})
ADD_EXECUTABLE (probe_unittest unit_test.cpp)
TARGET_LINK_LIBRARIES (probe_unittest probe ${GTEST_BOTH_LIBRARIES})
ADD_TEST (NAME probe_unit COMMAND probe_unittest)
SET(PROBE_BENCHMARKDIR ${CMAKE_CURRENT_BINARY_DIR})

ADD_EXECUTABLE (probe_benchmark probe_benchmark.cpp)
TARGET_LINK_LIBRARIES (probe_benchmark probe)

