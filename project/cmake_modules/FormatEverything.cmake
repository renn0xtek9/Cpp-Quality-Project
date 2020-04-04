# Additional targets to perform clang-format

# Get all project files IF (NOT CHECK_CXX_SOURCE_FILES) MESSAGE ( FATAL_ERROR
# "Variable CHECK_CXX_SOURCE_FILES not defined - set it to the list of files to
# auto-format" ) RETURN () ENDIF ()
#
# FOREACH (FILE ${CHECK_CXX_SOURCE_FILES}) STRING (REGEX REPLACE
# "${CMAKE_CURRENT_SOURCE_DIR}" "${CMAKE_CURRENT_BINARY_DIR}" STAMPFILE ${FILE})
# GET_FILENAME_COMPONENT (DIROFSTAMPFILE ${STAMPFILE} DIRECTORY)
# ADD_CUSTOM_COMMAND ( OUTPUT ${STAMPFILE}.stamp DEPENDS ${FILE} COMMAND
# ${CMAKE_COMMAND} -E make_directory ${DIROFSTAMPFILE} COMMAND /usr/bin/clang-
# format -i ${FILE} COMMAND ${CMAKE_COMMAND} -E touch "${STAMPFILE}.stamp"
# COMMENT "Formatting ${FILE} and stamping it with ${STAMPFILE}.stamp" VERBATIM)
# LIST (APPEND FORMAT_DEPENDENCIES ${STAMPFILE}.stamp) ENDFOREACH (FILE) BUG if
# a file get renamed, its dependencies remains and will create make[2]: *** No
# rule to make target '../probelibrary/include/wtf.h', needed by
# 'probelibrary/include/wtf.h.stamp'.  Stop.

# We reference a file that will never actually get created on purpose: we want
# this rule to be executed all the time !
ADD_CUSTOM_TARGET (
  create-format-rule ALL
  COMMENT "Create format make rule"
  DEPENDS
    ${CMAKE_BINARY_DIR}/CMakeFiles/create-format-rule.dir/create-format-rule-creation.log.stamp
)

SET (_exclude_pattern "third-party")
IF (TOP_BUILD)
  SET (_exclude_pattern "${_exclude_pattern};${CMAKE_SOURCE_DIR}/${TOP_BUILD}")
  MESSAGE (
    STATUS
      "here: TOP_BUILD------------------------------------------------\n ${TOP_BUILD} "
  )
ENDIF ()

# Mention has output but don't really produce it on purpose !
ADD_CUSTOM_COMMAND (
  OUTPUT
    ${CMAKE_BINARY_DIR}/CMakeFiles/create-format-rule.dir/create-format-rule-creation.log.stamp
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  COMMAND cmake -E make_directory ${CMAKE_BINARY_DIR}/CMakeFiles/format.dir
  COMMAND echo "Generate format rules"
  COMMAND
    python3
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake_modules/scripts/generate_format_rules.py
    --build-directory ${CMAKE_BINARY_DIR} --repository ${CMAKE_SOURCE_DIR}
    --cpp-format-tool "/usr/bin/clang-format -i" --exclude-pattern
    \"${_exclude_pattern}\"
    >${PROJECT_BINARY_DIR}/CMakeFiles/create-format-rule.dir/create-format-rule-creation.log
)

ADD_CUSTOM_TARGET (format ALL DEPENDS create-format-rule)
