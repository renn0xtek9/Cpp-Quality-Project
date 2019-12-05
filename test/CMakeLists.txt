ADD_EXECUTABLE (testexe test_main.cpp)
ADD_TEST (NAME test_one COMMAND $<TARGET_FILE:testexe> o)
ADD_TEST (NAME test_failing COMMAND $<TARGET_FILE:testexe> n)
ADD_TEST (NAME test_onceageina COMMAND $<TARGET_FILE:testexe> o)

# This is a workaround of a CMake bug which does not write build target for the
# "test" target thus cd build && rm -rf * && cmake .. && make test  will not
# work
ADD_CUSTOM_TARGET (
  specs
  COMMAND ${CMAKE_CTEST_COMMAND}
  DEPENDS testexe)
