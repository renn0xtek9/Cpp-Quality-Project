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
SET (DOCUMENTATION_OUTPUT_FOLDER "${CMAKE_CURRENT_BINARY_DIR}")
SET (ENV{DOCUMENTATION_OUTPUT_FOLDER} ${DOCUMENTATION_OUTPUT_FOLDER})
ADD_CUSTOM_COMMAND (
  OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/code-documentation/html/index.html
  DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/code-documentation.doxygen
  VERBATIM
  COMMAND doxygen ${CMAKE_CURRENT_SOURCE_DIR}/code-documentation.doxygen
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
  COMMENT "Building code documentation")
ADD_CUSTOM_TARGET (
  code_documentation
  SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/code-documentation.doxygen
  COMMENT "Target code documentation"
  DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/code-documentation/html/index.html)
