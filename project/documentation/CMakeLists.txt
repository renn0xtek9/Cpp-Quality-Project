INCLUDE(CreateLatexDocumentation)

SET(_software_intern_name "software-intern-development")
SET(SOFTWARE_INTERN_MAIN_TEX ${_software_intern_name}.tex)
SET(SOFTWARE_INTERN_RESOURCES_FILES ${CMAKE_CURRENT_SOURCE_DIR}/resources/project_or_company_logo.png)
SET(SOFTWARE_INTERN_BIBLIOGRAPHY library.bib)

CreateLatexDocumentaion("${_software_intern_name}" "${SOFTWARE_INTERN_MAIN_TEX}" "${SOFTWARE_INTERN_RESOURCES_FILES}" "${SOFTWARE_INTERN_BIBLIOGRAPHY}")

add_custom_target(documentation 
    DEPENDS ${_software_intern_name})

