CMAKE_MINIMUM_REQUIRED (VERSION 3.0)
ENABLE_TESTING ()
SET (EXENAME testcpp)
PROJECT (${EXENAME} LANGUAGES CXX)
SET (CMAKE_CXX_STANDARD 14)
SET (CMAKE_CXX_EXTENSIONS OFF)
SET (CMAKE_CXX_STANDARD_REQUIRED ON)

set (GIT_HASH "unknown") 
find_package(Git QUIET) 
if(GIT_FOUND)
    execute_process(COMMAND ${GIT_EXECTUABLE} log -1 --pretty-format:%h
    OUTPUT_VARIABLE GIT_HASH OUTPUT_STRIP_TRAILING_WHITESPACE ERROR_QUIET) 
endif()
# configure_file(${CMAKE_CURRENT_LIST_DIR}/version.hpp.
# ONLY_CMAKE_FIND_ROOT_PATH${TARGET_DIR}/version.hpp @ONLY)

# WARNING Bad approach ! (will only do it at configure time ) not for the
# CMAKELists because if you changed them it leads to reconfiguring but the
# others yes
# FILE (GLOB_RECURSE CMAKELISTS "CMakeLists.txt")
# FOREACH (FILE ${CMAKELISTS})
#   EXECUTE_PROCESS (COMMAND cmake-format -i ${FILE} ${FILE})
# ENDFOREACH (FILE)
FILE (GLOB_RECURSE HPP "*.hpp")
FILE (GLOB_RECURSE CPP "*.cpp")
FILE (GLOB_RECURSE C_H "*.h")
LIST (APPEND CHECK_CXX_SOURCE_FILES ${HPP} ${CPP} ${C_H})
LIST (FILTER CHECK_CXX_SOURCE_FILES EXCLUDE REGEX "${CMAKE_BINARY_DIR}/*")
# MESSAGE ("clang-format for: " ${CHECK_CXX_SOURCE_FILES})
# 
# FOREACH (FILE ${CHECK_CXX_SOURCE_FILES})
#   EXECUTE_PROCESS (COMMAND clang-format -i ${FILE})
# ENDFOREACH (FILE)

# Adding clang-format check and formatter if found
FIND_PROGRAM(CLANG_FORMAT "clang-format")
IF(CLANG_FORMAT)
    ADD_CUSTOM_TARGET(
        format
        COMMAND
        ${CLANG_FORMAT}
        -i
        -style=file
        ${CHECK_CXX_SOURCE_FILES}
        COMMENT "Auto formatting of all source files"
    )

    ADD_CUSTOM_TARGET(
        check-format
        COMMAND
        ${CLANG_FORMAT}
        -style=file
        -output-replacements-xml
        ${CHECK_CXX_SOURCE_FILES}
        # print output
        | tee ${CMAKE_BINARY_DIR}/check_format_file.txt | grep -c "replacement " |
                tr -d "[:cntrl:]" && echo " replacements necessary"
        # WARNING: fix to stop with error if there are problems
        COMMAND ! grep -c "replacement "
                  ${CMAKE_BINARY_DIR}/check_format_file.txt > /dev/null
        COMMENT "Checking format compliance"
    )
ENDIF()



ADD_SUBDIRECTORY (probelibrary)

ADD_SUBDIRECTORY (test)

ADD_EXECUTABLE (${EXENAME} main.cpp)
add_dependencies(${EXENAME} format)
TARGET_LINK_LIBRARIES (${EXENAME} probe)

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
