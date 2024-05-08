MACRO (CreateLatexDocument _name _texsrc _resources _bibliography)
  FIND_PROGRAM (BIBER biber)
  FIND_PROGRAM (PDFLATEX pdflatex)
  FIND_PROGRAM (MAKEINDEX makeindex)

  IF (${BIBER}-NOTFOUND)
    MESSAGE (FATAL_ERROR "biber not found!")
  ENDIF ()
  IF (${PDFLATEX}-NOTFOUND)
    MESSAGE (FATAL_ERROR "pdflatex not found!")
  ENDIF ()
  IF (${MAKEINDEX}-NOTFOUND)
    MESAGE (FATAL_ERROR "pdflatex not found!")
  ENDIF ()
  SET (_output_folder "${CMAKE_CURRENT_BINARY_DIR}/${_name}/")
  FILE (MAKE_DIRECTORY ${_output_folder})

  ADD_CUSTOM_TARGET (
    ${_name}
    DEPENDS ${_output_folder}/${_name}.pdf
    SOURCES ${_texsrcs})

  ADD_CUSTOM_COMMAND (
    OUTPUT ${_output_folder}/${_name}.bcf ${_output_folder}/${_name}.idx
           ${_output_folder}/${_name}.nlo
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    DEPENDS ${_texsrcs} ${_resources}
    # COMMAND cmake -E copy ${_resources} ${_output_folder}
    COMMAND cmake -E copy ${_texsrc} ${_output_folder}
    VERBATIM
    COMMAND ${PDFLATEX} -output-directory ${_output_folder}
            ${CMAKE_CURRENT_SOURCE_DIR}/${_name}.tex
    COMMENT "First pass software internal documentation")

  # Runnig biber on the .blg created by the firs pass of pdflatex
  ADD_CUSTOM_COMMAND (
    OUTPUT ${_output_folder}/${_name}.blg
    COMMENT "Running ${BIBER} on ${_output_folder}/${_name}.bcf"
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMAND ${BIBER} --input-directory ${_output_folder} --output-directory
            ${_output_folder} ${_name}.bcf
    DEPENDS ${_output_folder}/${_name}.bcf ${_bibliography})

  # Running the make_index
  SET (
    _index_output
    "${CMAKE_CURRENT_BINARY_DIR}/${_name}.ilg ${_output_folder}/${_name}.ind")
  ADD_CUSTOM_COMMAND (
    OUTPUT ${_index_output}
    DEPENDS ${_output_folder}/${_name}.idx
    COMMENT "Runnning ${MAKEINDEX} on ${_output_folder}/${_name}.idx"
    WORKING_DIRECTORY ${_output_folder}
    COMMAND ${MAKEINDEX} ${_name}.idx)

  # Running make_index for glossary and acronyms
  SET (
    _glossary_output
    "${_output_folder}/${_name}.nls ${_output_folder}/${_name}.ilg ${_output_folder}/${_name}.gls ${_output_folder}/${_name}.glo ${_output_folder}/${_name}.acr ${_output_folder}/${_name}.acn"
  )
  ADD_CUSTOM_COMMAND (
    OUTPUT ${_glossary_output}
    DEPENDS ${_output_folder}/${_name}.nlo
    WORKING_DIRECTORY ${_output_folder}
    COMMAND ${MAKEINDEX} ${_name}.nlo -s nomencl.ist -o ${_name}.nls
    COMMAND ${MAKEINDEX} -s ${_name}.ist -t ${_name}.glg -o ${_name}.gls
            ${_name}.glo
    COMMAND ${MAKEINDEX} -s ${_name}.ist -t ${_name}.alg -o ${_name}.acr
            ${_name}.acn)

  # The final pass
  ADD_CUSTOM_COMMAND (
    OUTPUT ${_output_folder}/${_name}.pdf
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    DEPENDS ${_output_folder}/${_name}.blg ${_index_output} ${_glossary_output}
    # COMMAND cmake -E copy ${_resources} ${_output_folder}
    VERBATIM
    COMMAND ${PDFLATEX} -output-directory ${_output_folder}
            ${_output_folder}/${_name}.tex
    COMMENT "Building software internal documentation")

ENDMACRO ()
