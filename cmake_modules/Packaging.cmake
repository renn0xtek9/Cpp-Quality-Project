INCLUDE (InstallRequiredSystemLibraries)
SET (CPACK_PACKAGE_NAME "${PROJECT_NAME}")
SET (CPACK_PACKAGE_VENDOR "company-name")
SET (CPACK_PACKAGE_DESCRIPTION_SUMMARY "${PROJECT_NAME} - Brief description")
SET (CPACK_PACKAGE_INSTALL_DIRECTORY "${PROJECT_NAME}")
SET (CPACK_PACKAGE_HOMEPAGE_URL "http://company-url")
SET (CPACK_PACKAGE_CONTACT "author@company-email.com")
SET (CPACK_DEBIAN_PACKAGE_DEPENDS "")
SET (CPACK_GENERATOR DEB)
SET (CPACK_RESOURCE_FILE_LICENSE ${CMAKE_SOURCE_DIR}/License.txt)

INCLUDE (CPack)
