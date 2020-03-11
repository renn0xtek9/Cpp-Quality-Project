PROJECT (workflow_testing
DESCRIPTION "Testing the workflow of the template project")
enable_testing()
add_test(NAME workflow_git_hash_fresh_configure 
    COMMAND /bin/bash ${CMAKE_CURRENT_SOURCE_DIR}/git_hash_fresh_configure.sh
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

