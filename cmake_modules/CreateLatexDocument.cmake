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
    SOURCES ${_texsrc})

  ADD_CUSTOM_COMMAND (
    OUTPUT ${_output_folder}/${_name}.pdf
    DEPENDS ${_texsrc} ${_resources} ${_bibliography}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generating ${_name}"
    VERBATIM
    COMMAND ${PDFLATEX} -output-directory ${_output_folder}
            ${CMAKE_CURRENT_SOURCE_DIR}/${_name}.tex
    COMMAND ${BIBER} --input-directory ${_output_folder} --output-directory
            ${_output_folder} ${_name}.bcf
    COMMAND cd ${_output_folder} && ${MAKEINDEX} ${_name}.idx
    COMMAND cd ${_output_folder} && ${MAKEINDEX} ${_name}.nlo -s nomencl.ist -o
            ${_name}.nls
    COMMAND cd ${_output_folder} && ${MAKEINDEX} -s ${_name}.ist -t ${_name}.glg
            -o ${_name}.gls ${_name}.glo
    COMMAND cd ${_output_folder} && ${MAKEINDEX} -s ${_name}.ist -t ${_name}.alg
            -o ${_name}.acr ${_name}.acn
    COMMAND ${PDFLATEX} -output-directory ${_output_folder}
            ${CMAKE_CURRENT_SOURCE_DIR}/${_name}.tex)

ENDMACRO ()
