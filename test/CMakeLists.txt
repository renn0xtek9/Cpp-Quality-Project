add_executable(testexe test_main.cpp)
add_test(NAME test_one COMMAND $<TARGET_FILE:testexe> o)
add_test(NAME test_failing COMMAND $<TARGET_FILE:testexe> n)
add_test(NAME test_onceageina COMMAND $<TARGET_FILE:testexe> o)

#This is a workaround of a CMake bug which does not write build target for the "test" target thus cd build && rm -rf * && cmake .. && make test  will not work
add_custom_target(
  specs
  COMMAND ${CMAKE_CTEST_COMMAND}
  DEPENDS testexe)
