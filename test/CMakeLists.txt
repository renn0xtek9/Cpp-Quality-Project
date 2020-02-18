ADD_EXECUTABLE (testexe test_main.cpp)
ADD_TEST (NAME showcase_ctest_using_a_custom_exe_succeeding
          COMMAND $<TARGET_FILE:testexe> o)
ADD_TEST (NAME showcase_ctest_using_a_custom_exe_failing
          COMMAND $<TARGET_FILE:testexe> n)

FIND_PACKAGE (GTest REQUIRED)

ADD_EXECUTABLE (test_gtest_based test_gtest_based.cpp)
TARGET_LINK_LIBRARIES (test_gtest_based ${GTEST_BOTH_LIBRARIES})
ADD_TEST (NAME show_case_ctest_using_a_gtest_exe COMMAND $<TARGET_FILE:testexe>)

ADD_TEST (
  NAME show_case_ctest_using_a_bash_script
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
  COMMAND /bin/bash ${CMAKE_CURRENT_SOURCE_DIR}/test_script.sh)

# This is a workaround of a CMake bug which does not write build target for the
# "test" target thus cd build && rm -rf * && cmake .. && make test  will not
# work ADD_CUSTOM_TARGET ( specs COMMAND ${CMAKE_CTEST_COMMAND} DEPENDS testexe
# test_gtest_based)
