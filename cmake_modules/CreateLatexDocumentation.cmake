MACRO (CreateLatexDocumentaion _name _texsrc _resources _bibliography)
  FIND_PROGRAM (BIBER biber)
  FIND_PROGRAM (PDFLATEX pdflatex)
  FIND_PROGRAM (MAKEINDEX makeindex)

  # message(FATAL_ERROR ${BIBER})
  IF (${BIBER}-NOTFOUND)
    MESSAGE (
      FATAL_ERROR
        "biber not found! run install-doc-dep.sh to install documentation build dependencies!"
    )
  ENDIF ()
  IF (${PDFLATEX}-NOTFOUND)
    MESSAGE (
      FATAL_ERROR
        "pdflatex not found! run install-doc-dep.sh to install documentation build dependencies!"
    )
  ENDIF ()
  IF (${MAKEINDEX}-NOTFOUND)
    MESAGE (
      FATAL_ERROR
      "pdflatex not found! run install-doc-dep.sh to install documentation build dependencies!"
    )
  ENDIF ()

  ADD_CUSTOM_TARGET (
    ${_name}
    DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/${_name}.pdf
    SOURCES ${_texsrcs})

  ADD_CUSTOM_COMMAND (
    OUTPUT
      ${CMAKE_CURRENT_BINARY_DIR}/${_name}.bcf
      ${CMAKE_CURRENT_BINARY_DIR}/${_name}.idx
      ${CMAKE_CURRENT_BINARY_DIR}/${_name}.nlo
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    DEPENDS ${_texsrcs} ${_resources}
    COMMAND cmake -E copy ${_resources} ${CMAKE_CURRENT_BINARY_DIR}
    VERBATIM
    COMMAND ${PDFLATEX} -output-directory ${CMAKE_CURRENT_BINARY_DIR}
            ${CMAKE_CURRENT_SOURCE_DIR}/${_name}.tex
    COMMENT "First pass software internal documentation")

  # Runnig biber on the .blg created by the firs pass of pdflatex
  ADD_CUSTOM_COMMAND (
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${_name}.blg
    COMMENT "Running ${BIBER} on ${CMAKE_CURRENT_BINARY_DIR}/${_name}.bcf"
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMAND ${BIBER} --input-directory ${CMAKE_CURRENT_BINARY_DIR} ${_name}.bcf
    DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/${_name}.bcf ${_bibliography})

  # Running the make_index
  SET (
    _index_output
    "${CMAKE_CURRENT_BINARY_DIR}/${_name}.ilg ${CMAKE_CURRENT_BINARY_DIR}/${_name}.ind"
  )
  ADD_CUSTOM_COMMAND (
    OUTPUT ${_index_output}
    DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/${_name}.idx
    COMMENT "Runnning ${MAKEINDEX} on ${CMAKE_CURRENT_BINARY_DIR}/${_name}.idx"
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    COMMAND ${MAKEINDEX} ${_name}.idx)

  # Running make_index for glossary and acronyms
  SET (
    _glossary_output
    "${CMAKE_CURRENT_BINARY_DIR}/${_name}.nls ${CMAKE_CURRENT_BINARY_DIR}/${_name}.ilg ${CMAKE_CURRENT_BINARY_DIR}/${_name}.gls ${CMAKE_CURRENT_BINARY_DIR}/${_name}.glo ${CMAKE_CURRENT_BINARY_DIR}/${_name}.acr ${CMAKE_CURRENT_BINARY_DIR}/${_name}.acn"
  )
  ADD_CUSTOM_COMMAND (
    OUTPUT ${_glossary_output}
    DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/${_name}.nlo
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    COMMAND ${MAKEINDEX} ${_name}.nlo -s nomencl.ist -o ${_name}.nls
    COMMAND ${MAKEINDEX} -s ${_name}.ist -t ${_name}.glg -o ${_name}.gls
            ${_name}.glo
    COMMAND ${MAKEINDEX} -s ${_name}.ist -t ${_name}.alg -o ${_name}.acr
            ${_name}.acn)

  # The final pass
  ADD_CUSTOM_COMMAND (
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${_name}.pdf
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/${_name}.blg ${_index_output}
            ${_glossary_output}
    COMMAND cmake -E copy ${_resources} ${CMAKE_CURRENT_BINARY_DIR}
    VERBATIM
    COMMAND ${PDFLATEX} -output-directory ${CMAKE_CURRENT_BINARY_DIR}
            ${CMAKE_CURRENT_SOURCE_DIR}/${_name}.tex
    COMMENT "Building software internal documentation")

ENDMACRO ()
