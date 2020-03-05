#!/usr/bin/env python3
from generate_format_rules import FormatRuleCreator
import unittest
import os

builddirectory = None
relevant_file_extensions = None


class Testclassname(unittest.TestCase):
    def setUp(self):
        self.maxDiff=None
        self.m_format_rule_creator = FormatRuleCreator("build", "/home/foo/bar/",cpp_format_tool="/usr/bin/clang-format -i")
        self.current_file_directory = os.path.dirname(os.path.abspath(__file__))
        pass

    def test_GetFirstLineOfStampRecipe(self):
        self.assertEqual("main.cpp.stamp: ../main.cpp",
                         self.m_format_rule_creator._GetFirstLineOfStampRecipe("/home/foo/bar/main.cpp"))

    def test_GetFirstLineOfStampRecipe_source_in_subfolder(self):
        self.assertEqual("subfolder/main.cpp.stamp: ../subfolder/main.cpp",
                         self.m_format_rule_creator._GetFirstLineOfStampRecipe("/home/foo/bar/subfolder/main.cpp"))

    def test_GetSecondLineOfStampRecipe(self):
        self.assertEqual("\t@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/foo/bar/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_12) \"Formatting main.cpp and stamping it with /home/foo/bar/build/main.cpp.stamp\"",
                         self.m_format_rule_creator._GetSecondLineOfStampRecipe("/home/foo/bar/main.cpp", 12))

    def test_GetThirdLineOfStampRecipe(self):
        expected_directory="/home/foo/bar/build/lib/src"
        self.assertEqual("\t/usr/bin/cmake -E make_directory "+expected_directory,
                         self.m_format_rule_creator._GetThirdLineOfStampRecipe("/home/foo/bar/lib/src/main.cpp"))
        
    def test_GetFourthLineOfStampRecipe_cpp_file(self):
        sourcefile="/home/foo/bar/lib/src/main.cpp"
        expected_line="\t/usr/bin/clang-format -i /home/foo/bar/lib/src/main.cpp"
        self.assertEqual(expected_line,self.m_format_rule_creator._GetFourthLineOfStampeRecipe(sourcefile))
    
    def test_GetFourthLineOfStampRecipe_unknown_file_tyoe(self):
        sourcefile="/home/foo/bar/lib/src/main.wtf"
        expected_line="\techo \"No known formatting tool for /home/foo/bar/lib/src/main.wtf\""
        self.assertEqual(expected_line,self.m_format_rule_creator._GetFourthLineOfStampeRecipe(sourcefile))
    
    def test_GetFourthLineOfStampRecipe_python_file(self):
        sourcefile="/home/foo/bar/lib/src/script.py"
        self.m_format_rule_creator.python_format_tool="/usr/bin/autopep8 -i"
        expected_line="\t/usr/bin/autopep8 -i /home/foo/bar/lib/src/script.py"
        self.assertEqual(expected_line,self.m_format_rule_creator._GetFourthLineOfStampeRecipe(sourcefile))
        
    def test_GetFourthLineOfStampRecipe_python_file_but_unspecified_tool(self):
        sourcefile="/home/foo/bar/lib/src/script.py"
        expected_line="\techo \"No known formatting tool for /home/foo/bar/lib/src/script.py\""
        self.assertEqual(expected_line,self.m_format_rule_creator._GetFourthLineOfStampeRecipe(sourcefile))
    
    def test_GetFifthLineOfStampRecipe(self):
        sourcefile="/home/foo/bar/lib/src/main.cpp"
        expected_line="\t/usr/bin/cmake -E touch /home/foo/bar/build/lib/src/main.cpp.stamp"
        self.assertEqual(expected_line,self.m_format_rule_creator._GetFifthLineOfStampRecipe(sourcefile))

    def test_GetCMakeFilesFormatContent(self):
        self.assertEqual(["CMakeFiles/format: foobar.cpp.stamp"],
                         self.m_format_rule_creator._GetCMakeFilesFormatContent(["foobar.cpp"]))

    def test_GetCMakeFilesFormatContent_in_subfolder(self):
        self.assertEqual(["CMakeFiles/format: foo/bar.cpp.stamp"],
                         self.m_format_rule_creator._GetCMakeFilesFormatContent(["foo/bar.cpp"]))

    def test_GetListOfAbsolutePathOfRelevantFiles(self):
        test_repository = os.sep.join(
            [self.current_file_directory, "generate_format_rules_tests", "resources", "repository1"])
        test_builddirectory = os.sep.join([test_repository, "build"])
        self.m_format_rule_creator = FormatRuleCreator(test_builddirectory, test_repository)
        self.assertEqual([os.sep.join([test_repository, "foo.cpp"]),
                          os.sep.join([test_repository, "src", "foobar.cpp"]),
                          os.sep.join([test_repository, "bar.cpp"])], self.m_format_rule_creator._GetListOfAbsolutePathOfRelevantFiles())

    def test_GetArrayOfLinesForStampRecipe(self):
        expected_content=['main.cpp.stamp: ../main.cpp',
        '	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/foo/bar/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Formatting main.cpp and stamping it with /home/foo/bar/build/main.cpp.stamp"',
        '	/usr/bin/cmake -E make_directory /home/foo/bar/build',
        '	/usr/bin/clang-format -i /home/foo/bar/main.cpp',
        '	/usr/bin/cmake -E touch /home/foo/bar/build/main.cpp.stamp']
        content=self.m_format_rule_creator._GetArrayOfLinesForStampRecipe("/home/foo/bar/main.cpp",1)
        self.assertEqual(len(expected_content),len(content))
        for i in range(0,len(expected_content)):
            self.assertEqual(expected_content[i],content[i])
        



if __name__ == '__main__':
    unittest.main()
