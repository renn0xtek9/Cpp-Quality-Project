# Additional targets to perform clang-format

# Get all project files
IF (NOT CHECK_CXX_SOURCE_FILES)
  MESSAGE (
    FATAL_ERROR
      "Variable CHECK_CXX_SOURCE_FILES not defined - set it to the list of files to auto-format"
  )
  RETURN ()
ENDIF ()

FOREACH (FILE ${CHECK_CXX_SOURCE_FILES})
  STRING (REGEX REPLACE "${CMAKE_CURRENT_SOURCE_DIR}"
                        "${CMAKE_CURRENT_BINARY_DIR}" STAMPFILE ${FILE})
  GET_FILENAME_COMPONENT (DIROFSTAMPFILE ${STAMPFILE} DIRECTORY)
  ADD_CUSTOM_COMMAND (
    OUTPUT ${STAMPFILE}.stamp
    DEPENDS ${FILE}
    COMMAND ${CMAKE_COMMAND} -E make_directory ${DIROFSTAMPFILE}
    COMMAND /usr/bin/clang-format -i ${FILE}
    COMMAND ${CMAKE_COMMAND} -E touch "${STAMPFILE}.stamp"
    COMMENT "Formatting ${FILE} and stamping it with ${STAMPFILE}.stamp"
    VERBATIM)
  LIST (APPEND FORMAT_DEPENDENCIES ${STAMPFILE}.stamp)
ENDFOREACH (FILE)
# BUG if a file get renamed, its dependencies remains and will create make[2]:
# *** No rule to make target '../probelibrary/include/wtf.h', needed by
# 'probelibrary/include/wtf.h.stamp'.  Stop.
ADD_CUSTOM_TARGET (format ALL DEPENDS ${FORMAT_DEPENDENCIES})
