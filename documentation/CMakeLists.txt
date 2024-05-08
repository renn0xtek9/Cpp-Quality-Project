INCLUDE (CreateLatexDocument)

SET (requirements_document "requirements_document")
SET (REQUIREMENTS_DOCUMENT_MAIN_TEX ${requirements_document}.tex)
SET (REQUIREMENTS_DOCUMENTS_RESOURCES_FILES
     ${CMAKE_CURRENT_SOURCE_DIR}/resources/project_or_company_logo.png)
SET (REQUIREMENTS_DOCUMENTS_BIBLIOGRAPHY
     ${CMAKE_CURRENT_SOURCE_DIR}/library.bib)

CREATELATEXDOCUMENT (
  "${requirements_document}" "${REQUIREMENTS_DOCUMENT_MAIN_TEX}"
  "${REQUIREMENTS_DOCUMENTS_RESOURCES_FILES}"
  "${REQUIREMENTS_DOCUMENTS_BIBLIOGRAPHY}")

# Doxygen documentation
CONFIGURE_FILE (${CMAKE_CURRENT_SOURCE_DIR}/code_documentation.doxygen.in
                ${CMAKE_CURRENT_BINARY_DIR}/code_documentation.doxygen)
ADD_CUSTOM_COMMAND (
  OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/code_documentation/html/index.html
  DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/code_documentation.doxygen
  VERBATIM
  COMMAND doxygen ${CMAKE_CURRENT_BINARY_DIR}/code_documentation.doxygen
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
  COMMENT "Building code documentation")
ADD_CUSTOM_TARGET (
  code_documentation
  SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/code_documentation.doxygen.in
  DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/code_documentation/html/index.html)
