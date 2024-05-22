SET (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14 -pthread")
ADD_EXECUTABLE (probe_benchmark probe_benchmark.cpp)
TARGET_LINK_LIBRARIES (probe_benchmark probe)
