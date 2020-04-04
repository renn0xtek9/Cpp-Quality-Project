project(workflow_testing
        DESCRIPTION "Testing the workflow of the template project")
enable_testing()

add_test(
  NAME workflow_format_everything_script_unit_tests
  COMMAND /usr/bin/python3 test_generate_format_rules.py
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/project/cmake_modules/scripts)

add_test(
  NAME workflow_default_project_is_compiling
  COMMAND /bin/bash ${CMAKE_CURRENT_SOURCE_DIR}/default_project_is_compiling.sh
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

add_test(
  NAME workflow_build_in_correct_folder
  COMMAND /bin/bash ${CMAKE_CURRENT_SOURCE_DIR}/builds_in_correct_folder.sh
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

add_test(
  NAME workflow_git_hash_fresh_configure
  COMMAND /bin/bash ${CMAKE_CURRENT_SOURCE_DIR}/git_hash_fresh_configure.sh
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

add_test(
  NAME workflow_documentation_compiles_locally
  COMMAND /bin/bash ${CMAKE_CURRENT_SOURCE_DIR}/documentation_compile_locally.sh
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

add_test(
  NAME workflow_no_formatting_of_cmake_file_inside_build_directory_when_using_build_script
  COMMAND /bin/bash ${CMAKE_CURRENT_SOURCE_DIR}/no_formatting_of_cmake_file_inside_build_directory_when_using_build_script.sh
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})  

add_test(
  NAME workflow_no_formatting_of_cmake_file_inside_build_directory_when_using_cmake_directly
  COMMAND /bin/bash ${CMAKE_CURRENT_SOURCE_DIR}/no_formatting_of_cmake_file_inside_build_directory_when_using_cmake_directly.sh
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}) 
  
add_test(
  NAME workflow_no_formatting_of_source_file_inside_build_directory_when_using_build_script
  COMMAND /bin/bash ${CMAKE_CURRENT_SOURCE_DIR}/no_formatting_of_source_file_inside_build_directory_when_using_build_script.sh
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})  

add_test(
  NAME workflow_no_formatting_of_source_file_inside_build_directory_when_using_cmake_directly
  COMMAND /bin/bash ${CMAKE_CURRENT_SOURCE_DIR}/no_formatting_of_source_file_inside_build_directory_when_using_cmake_directly.sh
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}) 

