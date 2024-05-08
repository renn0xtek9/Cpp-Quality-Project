INCLUDE (CreateLatexDocumentation)

SET (requirements_documents "requirements_document")
SET (REQUIREMENTS_DOCUMENT_MAIN_TEX ${requirements_documents}.tex)
SET (REQUIREMENTS_DOCUMENTS_RESOURCES_FILES
     ${CMAKE_CURRENT_SOURCE_DIR}/resources/project_or_company_logo.png)
SET (REQUIREMENTS_DOCUMENTS_BIBLIOGRAPHY
     ${CMAKE_CURRENT_SOURCE_DIR}/library.bib)

CREATELATEXDOCUMENTAION (
  "${requirements_documents}" "${REQUIREMENTS_DOCUMENT_MAIN_TEX}"
  "${REQUIREMENTS_DOCUMENTS_RESOURCES_FILES}"
  "${REQUIREMENTS_DOCUMENTS_BIBLIOGRAPHY}")

ADD_CUSTOM_TARGET (
  requirements_engineering
  DEPENDS ${requirements_documents}
  COMMENT "Building requirements documentation")

SET (DOCUMENTATION_OUTPUT_FOLDER "${CMAKE_BINARY_DIR}/documentation")
SET (ENV{DOCUMENTATION_OUTPUT_FOLDER} ${DOCUMENTATION_OUTPUT_FOLDER})
FILE (MAKE_DIRECTORY ${DOCUMENTATION_OUTPUT_FOLDER})
ADD_CUSTOM_TARGET (
  code_documentation
  COMMAND doxygen ${CMAKE_CURRENT_SOURCE_DIR}/code-documentation.doxygen
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
  COMMENT "Building code documentation")
