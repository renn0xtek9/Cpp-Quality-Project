# WARNING Bad approach ! (will only do it at configure time ) not for the
# CMAKELists because if you changed them it leads to reconfiguring but the
# others yes
FILE (GLOB_RECURSE CMAKELISTS "CMakeLists.txt")
FOREACH (FILE ${CMAKELISTS})
  EXECUTE_PROCESS (COMMAND cmake-format -i ${FILE} ${FILE})
ENDFOREACH (FILE)
FILE (GLOB_RECURSE HPP "*.hpp")
FILE (GLOB_RECURSE CPP "*.cpp")
FILE (GLOB_RECURSE C_H "*.h")
LIST (APPEND CHECK_CXX_SOURCE_FILES ${HPP} ${CPP} ${C_H})
LIST (FILTER CHECK_CXX_SOURCE_FILES EXCLUDE REGEX "${CMAKE_BINARY_DIR}/*")
MESSAGE ("clang-format for: " ${CHECK_CXX_SOURCE_FILES})

FOREACH (FILE ${CHECK_CXX_SOURCE_FILES})
  EXECUTE_PROCESS (COMMAND clang-format -i ${FILE})
ENDFOREACH (FILE)
