#!/usr/bin/env python3
import sys
import os
import glob
import re
import codecs
import argparse

class FormatRuleCreator:
    def __init__(self, builddirectory, repository, cpp_format_tool=None,c_header_as_cpp=True, python_format_tool=None, qml_format_tool=None):
        self.repository = repository
        self.cpp_format_tool = cpp_format_tool
        self.python_format_tool = python_format_tool
        self.qml_format_tool = qml_format_tool
        self.builddirectory = builddirectory
        if not os.path.isabs(builddirectory):
            self.builddirectory = os.path.normpath(os.sep.join([self.repository, builddirectory]))
        self.relevant_extansions=list()
        if cpp_format_tool:
            self.relevant_extansions.extend(["hxx","cxx","cpp","hpp"])
            if c_header_as_cpp:
                self.relevant_extansions.extend(["h"])
        if python_format_tool:
            self.relevant_extansions.extend(["py"])
        if qml_format_tool:
            self.relevant_extansions.extend(["qml"])

    def _GetListOfAbsolutePathOfRelevantFiles(self):
        relevant_source_files = list()
        os.chdir(self.repository)
        files = glob.glob("**", recursive=True)
        for filepath in files:
            for extension in self.relevant_extansions:
                if filepath.split('.')[-1] == extension and not str(self.builddirectory+os.sep) in filepath:
                    relevant_source_files.append(os.sep.join([self.repository, filepath]))
        return relevant_source_files

    def _GetFullPathToSourceFileInsideTheBuildDirectory(self, sourcefile):
        path_inside_repository = os.path.commonpath([self.repository, os.path.abspath(sourcefile)])
        path_inside_builddirectory = os.path.abspath(sourcefile).replace(path_inside_repository, self.builddirectory)
        return path_inside_builddirectory

    def _GetStampFileAbsolutePath(self, sourcefile):
        return str("{}.stamp".format(self._GetFullPathToSourceFileInsideTheBuildDirectory(sourcefile)))


    def _GetFirstLineOfStampRecipe(self, sourcefile):
        return "{}.stamp: {}".format(os.path.relpath(sourcefile, self.repository), os.path.relpath(sourcefile, self.builddirectory))

    def _GetSecondLineOfStampRecipe(self, sourcefile, sourcefilenumber):
        return str("	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir={} --progress-num=$(CMAKE_PROGRESS_{}) \"Formatting {} and stamping it with {}\"".format(os.sep.join([self.builddirectory, "CMakeFiles"]), sourcefilenumber, os.path.basename(sourcefile), self._GetStampFileAbsolutePath(sourcefile)))

    def _GetThirdLineOfStampRecipe(self, sourcefile):
        """When call with /home/max/Projects/testcpp/foo/src/main.cpp, this will return something like 
        /usr/bin/cmake -E make_directory build/foo/src
        """
        # path_inside_repository=os.path.commonpath([self.repository,os.path.abspath(sourcefile)])
        # path_inside_builddirectory=os.path.abspath(sourcefile).replace(path_inside_repository,self.builddirectory)
        path_inside_builddirectory = self._GetFullPathToSourceFileInsideTheBuildDirectory(sourcefile)
        return str("\t/usr/bin/cmake -E make_directory "+os.path.abspath(os.path.join(path_inside_builddirectory, os.pardir)))

    def _GetFourthLineOfStampeRecipe(self, sourcefile):
        """When call with  /home/max/Projects/testcpp/foo/src/main.cpp, this will return 
        /usr/bin/clang-format -i /home/max/Projects/testcpp/foo/src/main.cpp"""
        extansion = sourcefile.split('.')[-1]
        if extansion in ["h", "hpp", "cpp", "cxx", "hxx"] and self.cpp_format_tool:
            return str("\t{} {}".format(self.cpp_format_tool, sourcefile))
        if extansion in ["py"] and self.python_format_tool:
            return str("\t{} {}".format(self.python_format_tool, sourcefile))
        if extansion in ["qml"] and self.qml_format_tool:
            return str("\t{} {}".format(self.python_format_tool, sourcefile))
        return str("\techo \"No known formatting tool for {}\"".format(sourcefile))

    def _GetFifthLineOfStampRecipe(self, sourcefile):
        return str("\t/usr/bin/cmake -E touch {}".format(os.path.abspath(self._GetStampFileAbsolutePath(sourcefile))))

    def _GetArrayOfLinesForStampRecipe(self, sourcefile, sourcefilenumber):
        content = list()
        content.append(self._GetFirstLineOfStampRecipe(sourcefile))
        content.append(self._GetSecondLineOfStampRecipe(sourcefile, sourcefilenumber))
        content.append(self._GetThirdLineOfStampRecipe(sourcefile))
        content.append(self._GetFourthLineOfStampeRecipe(sourcefile))
        content.append(self._GetFifthLineOfStampRecipe(sourcefile))
        return content
    
    def _GetStampRecipeSection(self):
        content=list()
        sourcefiles = self._GetListOfAbsolutePathOfRelevantFiles()
        for i in range(0,len(sourcefiles)):
            content.extend(self._GetArrayOfLinesForStampRecipe(sourcefiles[i],i))
            content.extend([""])
        return content

    def _GetCMakeFilesFormatContent(self, sourcefiles=list()):
        """This is the first block of the dynamically-written part of the build.make rule
        it produces ouptut like 
        CMakeFiles/format: foobar.cpp.stamp
        """
        content = list()
        for sourcefile in sourcefiles:
            content.append("CMakeFiles/format: "+sourcefile+".stamp")
        return content
    
    def _GetFormatStampLine(self,sourcefile):
        stampfile=self._GetStampFileAbsolutePath(sourcefile)
        stampfile_relative=os.path.relpath(stampfile,self.builddirectory)
        return str("format: {}".format(stampfile_relative))
    
    def _GetFormatStampBlock(self,sourcefiles):
        content=["format: CMakeFiles/format"]
        for source in sourcefiles:
            content.append(self._GetFormatStampLine(source))
        content.append("format: CMakeFiles/format.dir/build.make")
        return content

    def _DumpArrayOfLinesIntoOutputFile(self, content, outputfile, replacementdict=None, append_or_write="w"):
        with codecs.open(outputfile, append_or_write, encoding='utf_8') as file:
            file.write('\n'.join(content))

    def _DumpFileIntoOutputFile(self, inputfile, outputfile, replacementdict=None, append_or_write="w"):
        content = [line.rstrip('\n') for line in open(inputfile)]
        self._DumpArrayOfLinesIntoOutputFile(content, outputfile, None, append_or_write)
        
    def _GetMakeRuleFilePath(self):
        rule_make_file_list = [self.builddirectory, "CMakeFiles", "format.dir", "build.make"]
        return os.sep.join(rule_make_file_list)

    def WriteMakeFileOfFormattingRule(self):
        """This is the main function that will actually write the build.make for the formatting rule"""
        rule_make_file = self._GetMakeRuleFilePath()
        code_generation_directory = os.sep.join(["cmake_modules", "scripts"])
        self._DumpFileIntoOutputFile(os.sep.join(
            [code_generation_directory, "format_rules_header.in"]), rule_make_file, None, 'w')
        self._DumpArrayOfLinesIntoOutputFile(self._GetCMakeFilesFormatContent(
            self._GetListOfAbsolutePathOfRelevantFiles()), rule_make_file, None, 'a')
        self._DumpArrayOfLinesIntoOutputFile(self._GetStampRecipeSection())
        self._DumpArrayOfLinesIntoOutputFile(self._GetFormatStampBlock(self._GetListOfAbsolutePathOfRelevantFiles()))
        self._DumpFileIntoOutputFile(os.sep.join(
            [code_generation_directory, "format_rules_footer.in"]), rule_make_file, None, 'a')


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("-b","--build-directory",help="build directory",required=True)
    ap.add_argument("-r","--repository",help="repository",required=True)
    ap.add_argument("--cpp-format-tool",help="cpp file form",required=False)
    ap.add_argument("--python-format-tool",help="python file formatting command",required=False)
    ap.add_argument("--qml-format-tool",help="qml file formatting command",required=False)
    args = vars(ap.parse_args())
    
    

if __name__ == "__main__":
    main(sys.argv)
    
#useage
#./script.py --cpp-format-tool="/usr/bin/clang-format -i" \
#--python-format-tool="/usr/bin/autopep8 -i" \
#--c-header-as-cpp
