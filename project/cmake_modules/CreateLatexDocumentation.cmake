macro(CreateLatexDocumentaion _name _texsrc _resources _bibliography)
    find_program(BIBER biber)
    find_program(PDFLATEX pdflatex)
    find_program(MAKEINDEX makeindex)

    # message(FATAL_ERROR ${BIBER})
    if(${BIBER}-NOTFOUND)
        message(FATAL_ERROR "biber not found! run install-doc-dep.sh to install documentation build dependencies!")
    endif()
    if(${PDFLATEX}-NOTFOUND)
        message(FATAL_ERROR "pdflatex not found! run install-doc-dep.sh to install documentation build dependencies!")
    endif()
    if(${MAKEINDEX}-NOTFOUND)
        mesage(FATAL_ERROR "pdflatex not found! run install-doc-dep.sh to install documentation build dependencies!")
    endif()


    add_custom_target(${_name}
        DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/${_name}.pdf
        SOURCES ${_texsrcs})

    add_custom_command(
        OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${_name}.bcf ${CMAKE_CURRENT_BINARY_DIR}/${_name}.idx
        ${CMAKE_CURRENT_BINARY_DIR}/${_name}.nlo
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        DEPENDS ${_texsrcs} ${_resources}
        COMMAND cmake -E copy ${_resources} ${CMAKE_CURRENT_BINARY_DIR}
        VERBATIM
        COMMAND ${PDFLATEX} -output-directory ${CMAKE_CURRENT_BINARY_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/${_name}.tex 
        COMMENT "First pass software internal documentation")

    #Runnig biber on the .blg created by the firs pass of pdflatex
    add_custom_command(
        OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${_name}.blg
        COMMENT "Running ${BIBER} on ${CMAKE_CURRENT_BINARY_DIR}/${_name}.bcf"
        COMMAND ${BIBER} --input-directory ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR}/${_name}.bcf
        DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/${_name}.bcf ${_bibliography})
        
    #Running the make_index 
    SET(_index_output "${CMAKE_CURRENT_BINARY_DIR}/${_name}.ilg ${CMAKE_CURRENT_BINARY_DIR}/${_name}.ind")
    add_custom_command(
        OUTPUT ${_index_output}
        DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/${_name}.idx
        COMMENT "Runnning ${MAKEINDEX} on ${CMAKE_CURRENT_BINARY_DIR}/${_name}.idx"
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        COMMAND ${MAKEINDEX} ${_name}.idx)

    #Running make_index for glossary and acronyms
    SET(_glossary_output "${CMAKE_CURRENT_BINARY_DIR}/${_name}.nls ${CMAKE_CURRENT_BINARY_DIR}/${_name}.ilg ${CMAKE_CURRENT_BINARY_DIR}/${_name}.gls ${CMAKE_CURRENT_BINARY_DIR}/${_name}.glo ${CMAKE_CURRENT_BINARY_DIR}/${_name}.acr ${CMAKE_CURRENT_BINARY_DIR}/${_name}.acn")
    add_custom_command(
        OUTPUT ${_glossary_output}
        DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/${_name}.nlo
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        COMMAND ${MAKEINDEX} ${_name}.nlo -s nomencl.ist -o ${_name}.nls
        COMMAND ${MAKEINDEX} -s ${_name}.ist -t ${_name}.glg -o ${_name}.gls ${_name}.glo 
        COMMAND ${MAKEINDEX} -s ${_name}.ist -t ${_name}.alg -o ${_name}.acr ${_name}.acn)

    #The final pass 
    add_custom_command(
        OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${_name}.pdf 
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/${_name}.blg ${_index_output} ${_glossary_output}
        COMMAND cmake -E copy ${_resources} ${CMAKE_CURRENT_BINARY_DIR}
        VERBATIM
        COMMAND ${PDFLATEX} -output-directory ${CMAKE_CURRENT_BINARY_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/${_name}.tex 
        COMMENT "Building software internal documentation")
          
endmacro()
