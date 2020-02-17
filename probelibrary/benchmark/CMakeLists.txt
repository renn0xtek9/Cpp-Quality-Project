SET (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14 -pthread")
SET(PROBE_BENCHMARKDIR ${CMAKE_CURRENT_BINARY_DIR})
ADD_EXECUTABLE (probe_benchmark probe_benchmark.cpp)
TARGET_LINK_LIBRARIES (probe_benchmark probe)

