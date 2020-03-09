#!/usr/bin/env python3
import sys
import os
import glob
import re
import codecs
import argparse

class FormatRuleCreator:
    def __init__(self, builddirectory, repository, cpp_format_tool=None, c_header_as_cpp=True, python_format_tool=None, qml_format_tool=None):
        self.repository = repository
        self.cpp_format_tool = cpp_format_tool
        self.python_format_tool = python_format_tool
        self.qml_format_tool = qml_format_tool
        self.builddirectory = builddirectory
        if not os.path.isabs(builddirectory):
            self.builddirectory = os.path.normpath(os.sep.join([self.repository, builddirectory]))
        self.relevant_extansions = list()
        if cpp_format_tool:
            self.relevant_extansions.extend(["hxx", "cxx", "cpp", "hpp"])
            if c_header_as_cpp:
                self.relevant_extansions.extend(["h"])
        if python_format_tool:
            self.relevant_extansions.extend(["py"])
        if qml_format_tool:
            self.relevant_extansions.extend(["qml"])

    def __GetListOfAbsolutePathOfRelevantFiles(self):
        relevant_source_files = list()
        os.chdir(self.repository)
        files = glob.glob("**", recursive=True)
        for filepath in files:
            for extension in self.relevant_extansions:
                if filepath.split('.')[-1] == extension and not str(self.builddirectory+os.sep) in filepath:
                    relevant_source_files.append(os.sep.join([self.repository, filepath]))
        return relevant_source_files

    def __GetFullPathToSourceFileInsideTheBuildDirectory(self, sourcefile):
        path_inside_repository = os.path.commonpath([self.repository, os.path.abspath(sourcefile)])
        path_inside_builddirectory = os.path.abspath(sourcefile).replace(path_inside_repository, self.builddirectory)
        return path_inside_builddirectory

    def __GetStampFileAbsolutePath(self, sourcefile):
        return str("{}.stamp".format(self.
                                     __GetFullPathToSourceFileInsideTheBuildDirectory
                                     (sourcefile)))

    def __GetStampFileRelativePath(self, sourcefile):
        stampfile = self.__GetStampFileAbsolutePath(sourcefile)
        return os.path.relpath(stampfile, self.builddirectory)

    def __GetFirstLineOfStampRecipe(self, sourcefile):
        return "{}.stamp: {}".format(os.path.relpath(sourcefile, self.repository), os.path.relpath(sourcefile, self.builddirectory))

    def __GetSecondLineOfStampRecipe(self, sourcefile, sourcefilenumber):
        return str("	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir={} --progress-num=$(CMAKE_PROGRESS_{}) \"Formatting {} and stamping it with {}\"".format(os.sep.join([self.builddirectory, "CMakeFiles"]), sourcefilenumber, os.path.basename(sourcefile), self.__GetStampFileAbsolutePath(sourcefile)))

    def __GetThirdLineOfStampRecipe(self, sourcefile):
        """When call with /home/max/Projects/testcpp/foo/src/main.cpp, this will return something like 
        /usr/bin/cmake -E make_directory build/foo/src
        """
        # path_inside_repository=os.path.commonpath([self.repository,os.path.abspath(sourcefile)])
        # path_inside_builddirectory=os.path.abspath(sourcefile).replace(path_inside_repository,self.builddirectory)
        path_inside_builddirectory = self.__GetFullPathToSourceFileInsideTheBuildDirectory(sourcefile)
        return str("\t/usr/bin/cmake -E make_directory "+os.path.abspath(os.path.join(path_inside_builddirectory, os.pardir)))

    def __GetFourthLineOfStampeRecipe(self, sourcefile):
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

    def __GetFifthLineOfStampRecipe(self, sourcefile):
        return str("\t/usr/bin/cmake -E touch {}".format(os.path.abspath(self.__GetStampFileAbsolutePath(sourcefile))))

    def __GetArrayOfLinesForStampRecipe(self, sourcefile, sourcefilenumber):
        content = list()
        content.append(self.__GetFirstLineOfStampRecipe(sourcefile))
        content.append(self.__GetSecondLineOfStampRecipe(sourcefile, sourcefilenumber))
        content.append(self.__GetThirdLineOfStampRecipe(sourcefile))
        content.append(self.__GetFourthLineOfStampeRecipe(sourcefile))
        content.append(self.__GetFifthLineOfStampRecipe(sourcefile))
        return content

    def __GetStampRecipeSection(self):
        content = list()
        sourcefiles = self.__GetListOfAbsolutePathOfRelevantFiles()
        for i in range(0, len(sourcefiles)):
            content.extend(self.__GetArrayOfLinesForStampRecipe(sourcefiles[i], i))
            content.extend([""])
        return content

    def __GetCMakeFilesFormatContent(self, sourcefiles=list()):
        """This is the first block of the dynamically-written part of the build.make rule
        it produces ouptut like 
        CMakeFiles/format: foobar.cpp.stamp
        """
        content = list()
        for sourcefile in sourcefiles:
            content.append("CMakeFiles/format: "+self.__GetStampFileRelativePath(sourcefile))
        return content

    def __GetFormatStampLine(self, sourcefile):
        stampfile = self.__GetStampFileAbsolutePath(sourcefile)
        stampfile_relative = os.path.relpath(stampfile, self.builddirectory)
        return str("format: {}".format(stampfile_relative))

    def __GetFormatStampBlock(self, sourcefiles):
        content = ["format: CMakeFiles/format"]
        for source in sourcefiles:
            content.append(self.__GetFormatStampLine(source))
        content.append("format: CMakeFiles/format.dir/build.make")
        return content

    def __DumpArrayOfLinesIntoOutputFile(self, content, outputfile, replacementdict=None, append_or_write="a"):
        with codecs.open(outputfile, append_or_write, encoding='utf_8') as file:
            file.write('\n'.join(content))

    def __DumpFileIntoOutputFile(self, inputfile, outputfile, replacementdict=None, append_or_write="a"):
        content = [line.rstrip('\n') for line in open(inputfile)]
        print("For input file"+inputfile + "  " + append_or_write + "----------" + outputfile)
        print("Dumping "+'\n'.join(content))
        self.__DumpArrayOfLinesIntoOutputFile(content, outputfile, None, append_or_write)

    def __GetMakeRuleFilePath(self):
        rule_make_file_list = [self.builddirectory, "CMakeFiles", "format.dir", "build.make"]
        return os.sep.join(rule_make_file_list)

    def __GetCodeGenerationDirectory(self):
        return os.path.dirname(os.path.abspath(__file__))

    def __WriteLineBreaksInOutputFile(self,
                                      number_of_line_breaks):
        rule_make_file = self.__GetMakeRuleFilePath()
        for i in range(0, number_of_line_breaks):
            self.__DumpArrayOfLinesIntoOutputFile(['\n'], rule_make_file, 'a')

    def WriteMakeFileOfFormattingRule(self):
        """This is the main function that will actually write the build.make for the formatting rule"""
        rule_make_file = self.__GetMakeRuleFilePath()
        code_generation_directory = self.__GetCodeGenerationDirectory()
        self.__DumpFileIntoOutputFile(os.sep.join(
            [code_generation_directory, "format_rules_header.in"]), rule_make_file, None, 'w')
        self.__WriteLineBreaksInOutputFile(2)
        self.__DumpArrayOfLinesIntoOutputFile(self.__GetCMakeFilesFormatContent(
            self.__GetListOfAbsolutePathOfRelevantFiles()), rule_make_file, None, 'a')
        self.__WriteLineBreaksInOutputFile(2)
        self.__DumpArrayOfLinesIntoOutputFile(self.__GetStampRecipeSection(), rule_make_file, None, 'a')
        self.__WriteLineBreaksInOutputFile(2)
        self.__DumpArrayOfLinesIntoOutputFile(self.__GetFormatStampBlock(
            self.__GetListOfAbsolutePathOfRelevantFiles()), rule_make_file, None, 'a')
        self.__WriteLineBreaksInOutputFile(2)
        self.__DumpFileIntoOutputFile(os.sep.join(
            [code_generation_directory, "format_rules_footer.in"]), rule_make_file, None, 'a')


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("-b", "--build-directory", help="build directory", required=True)
    ap.add_argument("-r", "--repository", help="repository", required=True)
    ap.add_argument("--cpp-format-tool", help="cpp file form", required=False)
    ap.add_argument("--c-header-as-cpp", help="c header ('*.h') are treated as cpp headers", required=False)
    ap.add_argument("--python-format-tool", help="python file formatting command", required=False)
    ap.add_argument("--qml-format-tool", help="qml file formatting command", required=False)
    args = vars(ap.parse_args())

    creator = FormatRuleCreator(args['build_directory'], args['repository'], cpp_format_tool=args['cpp_format_tool'],
                                c_header_as_cpp=args['c_header_as_cpp'], python_format_tool=args['python_format_tool'],
                                qml_format_tool=args['qml_format_tool'])
    creator.WriteMakeFileOfFormattingRule()


if __name__ == "__main__":
    main(sys.argv)
