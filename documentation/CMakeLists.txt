INCLUDE (CreateLatexDocumentation)

SET (requirements_documents "requirements_document")
SET (SOFTWARE_INTERN_MAIN_TEX ${requirements_documents}.tex)
SET (SOFTWARE_INTERN_RESOURCES_FILES
     ${CMAKE_CURRENT_SOURCE_DIR}/resources/project_or_company_logo.png)
SET (SOFTWARE_INTERN_BIBLIOGRAPHY ${CMAKE_CURRENT_SOURCE_DIR}/library.bib)

CREATELATEXDOCUMENTAION (
  "${requirements_documents}" "${SOFTWARE_INTERN_MAIN_TEX}"
  "${SOFTWARE_INTERN_RESOURCES_FILES}" "${SOFTWARE_INTERN_BIBLIOGRAPHY}")

ADD_CUSTOM_TARGET (
  documentation
  DEPENDS ${requirements_documents}
  COMMENT "Building requirements documentation")
