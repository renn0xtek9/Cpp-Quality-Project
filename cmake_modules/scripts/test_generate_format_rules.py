#!/usr/bin/env python3
from generate_format_rules import FormatRuleCreator
import unittest
import os

builddirectory=None
relevant_file_extensions=None

class Testclassname(unittest.TestCase):
    def setUp(self):
        self.m_format_rule_creator=FormatRuleCreator("build","/home/foo/bar/")
        pass
    
    def test_FullPathToSourcePath_relative_build_relative_source_absolute_repo(self):
        self.assertEqual("/home/foo/bar/main.cpp",self.m_format_rule_creator.AsbolutePathToSourceFile("build","main.cpp","/home/foo/bar/"))
    
    def test_FullPathToSourcePath_relative_build_absolute_source_absolute_repo(self):
        self.assertEqual("/home/foo/bar/main.cpp",self.m_format_rule_creator.AsbolutePathToSourceFile("build","/home/foo/bar/main.cpp","/home/foo/bar/"))
        
    def test_FullPathToSourcePath_absolute_build_relative_source_absolute_repo(self):
        self.assertEqual("/home/foo/bar/main.cpp",self.m_format_rule_creator.AsbolutePathToSourceFile("build","main.cpp","/home/foo/bar/"))
        
    def test_FullPathToSourcePath_outsource_build_relative_source_absolute_repo(self):
        self.assertEqual("/home/foo/bar/main.cpp",self.m_format_rule_creator.AsbolutePathToSourceFile("/tmp/build","main.cpp","/home/foo/bar/"))
        
    def test_FullPathToSourcePath_outsource_build_relative_source_in_subfolder_absolute_repo(self):
        self.assertEqual("/home/foo/bar/subfolder/main.cpp",self.m_format_rule_creator.AsbolutePathToSourceFile("/tmp/build","subfolder/main.cpp","/home/foo/bar/"))
        
    def test_GetFirstLineOfStampRecipe(self):
        self.assertEqual("main.cpp.stamp: /home/foo/bar/main.cpp",self.m_format_rule_creator.GetFirstLineOfStampRecipe("main.cpp"))
        
    def test_GetFirstLineOfStampRecipe_source_in_subfolder(self):
        self.assertEqual("subfolder/main.cpp.stamp: /home/foo/bar/subfolder/main.cpp",self.m_format_rule_creator.GetFirstLineOfStampRecipe("subfolder/main.cpp"))
        
        
    def test_GetSecondLineOfStampRecipe(self):
        self.assertEqual("\t@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/max/Projects/testcpp/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_12) \"Formatting /home/max/Projects/testcpp/main.cpp and stamping it with /home/max/Projects/testcpp/build/main.cpp.stamp\"",self.m_format_rule_creator.GetSecondLineOfStampRecipe("main.cpp",12))
        
    def test_GetCMakeFilesFormatContent(self):
        self.assertEqual(["CMakeFiles/format: foobar.cpp.stamp"],self.m_format_rule_creator.GetCMakeFilesFormatContent(["foobar.cpp"]))
        
    def test_GetCMakeFilesFormatContent_in_subfolder(self):
        self.assertEqual(["CMakeFiles/format: foo/bar.cpp.stamp"],self.m_format_rule_creator.GetCMakeFilesFormatContent(["foo/bar.cpp"]))
        
    def test_GetListOfAbsolutePathOfRelevantFiles(self):
        current_file_directory=os.path.dirname(os.path.abspath(__file__))
        test_repository=os.sep.join([current_file_directory,"generate_format_rules_test","resources","repository1"])
        test_builddirectory=os.sep.join([test_repository,"build"])
        self.m_format_rule_creator=FormatRuleCreator(test_builddirectory,test_repository)
        self.assertEqual([os.sep.join([test_repository,"foo.cpp"]),
                          os.sep.join([test_repository,"bar.cpp"]),
                          os.sep.join([test_repository,"src","foobar.cpp"])],self.m_format_rule_creator.GetListOfAbsolutePathOfRelevantFiles())
    
        
        
if __name__ == '__main__':
    unittest.main()
            
            
            
