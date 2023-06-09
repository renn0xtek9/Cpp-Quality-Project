#!/usr/bin/env python3
from generate_format_rules import FormatRuleCreator
import unittest
import os
import sys

g_current_file_directory=os.path.dirname(os.path.abspath(__file__))
g_directory_from_where_the_script_was_called=os.getcwd()



class FormatRuleCreator_FileIntegrity(unittest.TestCase):
    def setUp(self):
        global g_directory_from_where_the_script_was_called, g_current_file_directory
        self.maxDiff=None
        self.m_unit = FormatRuleCreator("build", "/home/foo/bar/",cpp_format_tool="/usr/bin/clang-format -i")
        self.current_file_directory = g_current_file_directory
        os.chdir(g_directory_from_where_the_script_was_called)
        pass
    
    def test_GetFormatStampLine(self):
        sourcefile="/home/foo/bar/lib/src/file.cpp"
        expected_content="format: lib/src/file.cpp.stamp"
        self.assertEqual(expected_content,self.m_unit._FormatRuleCreator__GetFormatStampLine(sourcefile))
        
    def test_GetFormatStampBlock(self):
        sourcefiles=["/home/foo/bar/lib/src/file.cpp","/home/foo/bar/main.cpp"]
        expected=["format: CMakeFiles/format",
        "format: lib/src/file.cpp.stamp",
        "format: main.cpp.stamp",
        "format: CMakeFiles/format.dir/build.make"]
        self.assertEqual(expected,self.m_unit._FormatRuleCreator__GetFormatStampBlock(sourcefiles))
        
    def test_GetArrayOfLinesForStampRecipe(self):
        expected_content=['main.cpp.stamp: ../main.cpp',
        '	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/foo/bar/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Formatting main.cpp and stamping it with /home/foo/bar/build/main.cpp.stamp"',
        '	/usr/bin/cmake -E make_directory /home/foo/bar/build',
        '	/usr/bin/clang-format -i /home/foo/bar/main.cpp',
        '	/usr/bin/cmake -E touch /home/foo/bar/build/main.cpp.stamp']
        content=self.m_unit._FormatRuleCreator__GetArrayOfLinesForStampRecipe("/home/foo/bar/main.cpp",1)
        self.assertEqual(len(expected_content),len(content))
        for i in range(0,len(expected_content)):
            self.assertEqual(expected_content[i],content[i])
    
    def test_GetFirstLineOfStampRecipe(self):
        self.assertEqual("main.cpp.stamp: ../main.cpp",
                         self.m_unit._FormatRuleCreator__GetFirstLineOfStampRecipe("/home/foo/bar/main.cpp"))

    def test_GetFirstLineOfStampRecipe_source_in_subfolder(self):
        self.assertEqual("subfolder/main.cpp.stamp: ../subfolder/main.cpp",
                         self.m_unit._FormatRuleCreator__GetFirstLineOfStampRecipe("/home/foo/bar/subfolder/main.cpp"))

    def test_GetSecondLineOfStampRecipe(self):
        self.assertEqual("\t@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/foo/bar/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_12) \"Formatting main.cpp and stamping it with /home/foo/bar/build/main.cpp.stamp\"",
                         self.m_unit._FormatRuleCreator__GetSecondLineOfStampRecipe("/home/foo/bar/main.cpp", 12))

    def test_GetThirdLineOfStampRecipe(self):
        expected_directory="/home/foo/bar/build/lib/src"
        self.assertEqual("\t/usr/bin/cmake -E make_directory "+expected_directory,
                         self.m_unit._FormatRuleCreator__GetThirdLineOfStampRecipe("/home/foo/bar/lib/src/main.cpp"))
        
    def test_GetFourthLineOfStampRecipe_cpp_file(self):
        sourcefile="/home/foo/bar/lib/src/main.cpp"
        expected_line="\t/usr/bin/clang-format -i /home/foo/bar/lib/src/main.cpp"
        self.assertEqual(expected_line,self.m_unit._FormatRuleCreator__GetFourthLineOfStampeRecipe(sourcefile))
    
    def test_GetFourthLineOfStampRecipe_unknown_file_tyoe(self):
        sourcefile="/home/foo/bar/lib/src/main.wtf"
        expected_line="\techo \"No known formatting tool for /home/foo/bar/lib/src/main.wtf\""
        self.assertEqual(expected_line,self.m_unit._FormatRuleCreator__GetFourthLineOfStampeRecipe(sourcefile))
    
    def test_GetFourthLineOfStampRecipe_python_file(self):
        sourcefile="/home/foo/bar/lib/src/script.py"
        self.m_unit.python_format_tool="/usr/bin/autopep8 -i"
        expected_line="\t/usr/bin/autopep8 -i /home/foo/bar/lib/src/script.py"
        self.assertEqual(expected_line,self.m_unit._FormatRuleCreator__GetFourthLineOfStampeRecipe(sourcefile))
        
    def test_GetFourthLineOfStampRecipe_python_file_but_unspecified_tool(self):
        sourcefile="/home/foo/bar/lib/src/script.py"
        expected_line="\techo \"No known formatting tool for /home/foo/bar/lib/src/script.py\""
        self.assertEqual(expected_line,self.m_unit._FormatRuleCreator__GetFourthLineOfStampeRecipe(sourcefile))
    
    def test_GetFifthLineOfStampRecipe(self):
        sourcefile="/home/foo/bar/lib/src/main.cpp"
        expected_line="\t/usr/bin/cmake -E touch /home/foo/bar/build/lib/src/main.cpp.stamp"
        self.assertEqual(expected_line,self.m_unit._FormatRuleCreator__GetFifthLineOfStampRecipe(sourcefile))
    


class FormatRuleCreator_HelperFunctions(unittest.TestCase):
    def setUp(self):
        global g_directory_from_where_the_script_was_called, g_current_file_directory
        self.maxDiff=None
        self.m_unit = FormatRuleCreator("build", "/home/foo/bar/",cpp_format_tool="/usr/bin/clang-format -i",excludepattern="third-party")
        self.current_file_directory = g_current_file_directory
        os.chdir(g_directory_from_where_the_script_was_called)
        pass
    
    def test_GetCMakeFilesFormatContent(self):
        self.assertEqual(["CMakeFiles/format: foobar.cpp.stamp"],
                         self.m_unit._FormatRuleCreator__GetCMakeFilesFormatContent(["/home/foo/bar/foobar.cpp"]))

    def test_GetCMakeFilesFormatContent_in_subfolder(self):
        self.assertEqual(["CMakeFiles/format: foo/bar.cpp.stamp"],
                         self.m_unit._FormatRuleCreator__GetCMakeFilesFormatContent(["/home/foo/bar/foo/bar.cpp"]))

    def test_GetListOfAbsolutePathOfRelevantFiles(self):        
        test_repository = os.sep.join(
            [self.current_file_directory, "generate_format_rules_tests", "resources", "repository1"])
        test_builddirectory = os.sep.join([test_repository, "build"])
        self.m_unit = FormatRuleCreator(test_builddirectory, test_repository,cpp_format_tool="/usr/bin/clang -i",excludepattern="third-party")
        self.assertEqual([os.sep.join([test_repository, "bar.cpp"]),
                          os.sep.join([test_repository, "foo.cpp"]),                          
                          os.sep.join([test_repository, "src", "foobar.cpp"])], self.m_unit._FormatRuleCreator__GetListOfAbsolutePathOfRelevantFiles())
        
    def test_GetListOfAbsolutePathOfRelevantFiles_ExcludesFilesThatAreInBuildOfOtherPlatform(self):
        test_repository = os.sep.join(
            [self.current_file_directory, "generate_format_rules_tests", "resources", "repository1"])
        test_builddirectory = os.sep.join([test_repository, "build/debug-someplatform"])
        self.m_unit = FormatRuleCreator(test_builddirectory, test_repository,cpp_format_tool="/usr/bin/clang -i",excludepattern="third-party;build")
        self.assertEqual([os.sep.join([test_repository, "bar.cpp"]),
                          os.sep.join([test_repository, "foo.cpp"]),                          
                          os.sep.join([test_repository, "src", "foobar.cpp"])], self.m_unit._FormatRuleCreator__GetListOfAbsolutePathOfRelevantFiles())
        
    def test_GetListOfAbsolutePathOfRelevantFiles_ExcludesFilesThatAreInBuildOfOtherPlatform_WhenScriptNotCalledInRepositoryDirectory(self):
        test_repository = os.sep.join(
            [self.current_file_directory, "generate_format_rules_tests", "resources", "repository1"])
        test_builddirectory = os.sep.join([test_repository, "build/debug-someplatform"])
        os.chdir(test_builddirectory)
        self.m_unit = FormatRuleCreator(test_builddirectory, test_repository,cpp_format_tool="/usr/bin/clang -i",excludepattern="third-party;build")
        self.assertEqual([os.sep.join([test_repository, "bar.cpp"]),
                          os.sep.join([test_repository, "foo.cpp"]),                          
                          os.sep.join([test_repository, "src", "foobar.cpp"])], self.m_unit._FormatRuleCreator__GetListOfAbsolutePathOfRelevantFiles())
        
    def test_RelevantExtansionFilesSetAutomaticaly(self):
        unit=FormatRuleCreator("build", "/home/foo/bar/",cpp_format_tool="/usr/bin/clang-format -i")
        self.assertEqual(["hxx","cxx","cpp","hpp","h"],unit.relevant_extansions)
        

    def test_GetMakeRuleFilePath(self):
        self.assertEqual("/home/foo/bar/build/CMakeFiles/format.dir/build.make",self.m_unit._FormatRuleCreator__GetMakeRuleFilePath())
    
    def test_GetCodeGenerationDirectory(self):
        expected=os.sep.join([os.path.dirname(os.path.abspath(__file__))])
        self.assertEqual(expected,self.m_unit._FormatRuleCreator__GetCodeGenerationDirectory())
        
    def test_GetStampFileAbsolutePath(self):
        sourcefile="/home/foo/bar/main.cpp"
        expected="/home/foo/bar/build/main.cpp.stamp"
        self.assertEqual(expected,self.m_unit._FormatRuleCreator__GetStampFileAbsolutePath(sourcefile))
        
    def test_GetStampFileAbsolutePath_subdirectory(self):
        sourcefile="/home/foo/bar/lib/src/main.cpp"
        expected="/home/foo/bar/build/lib/src/main.cpp.stamp"
        self.assertEqual(expected,self.m_unit._FormatRuleCreator__GetStampFileAbsolutePath(sourcefile))
        
    def test_GetStampFileRelativePath(self):
        sourcefile="/home/foo/bar/main.cpp"
        expected="main.cpp.stamp"
        self.assertEqual(expected,self.m_unit._FormatRuleCreator__GetStampFileRelativePath(sourcefile))
        
    def test_GetStampFileRelativePath_subdirectory(self):
        sourcefile="/home/foo/bar/lib/src/main.cpp"
        expected="lib/src/main.cpp.stamp"
        self.assertEqual(expected,self.m_unit._FormatRuleCreator__GetStampFileRelativePath(sourcefile))


if __name__ == '__main__':
    unittest.main()
