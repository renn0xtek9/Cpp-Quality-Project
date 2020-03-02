import sys,os,glob,re,codecs




class FormatRuleCreator:
    def __init__(self,builddirectory,repository):
        self.builddirectory=builddirectory
        self.repository=repository

    def AsbolutePathToSourceFile(self,absolute_build_path,sourcefile,repository):
        if os.path.isabs(sourcefile):
            return os.path.normpath(sourcefile)
        if os.path.isabs(repository):
            return os.path.normpath(os.sep.join([repository,sourcefile]))
        return ""
    
    def GetListOfAbsolutePathOfRelevantFiles(self):
        relevant_source_files=list()
        relevant_file_extensions=".cpp;.h;.hpp"
        os.chdir(self.repository)
        files=glob.glob("**",recursive=True)
        for filepath in files:
            for extension in relevant_file_extensions.split(';'):
                if filepath.split('.')[-1]==extension.replace('.','') and not str(self.builddirectory+os.sep) in filepath :
                    relevant_source_files.append(os.sep.join([self.repository,filepath]))
        print(relevant_source_files)
        return relevant_source_files        
    
    def GetFirstLineOfStampRecipe(self,sourcefile):
        return "{}.stamp: {}".format(sourcefile,self.AsbolutePathToSourceFile(self.builddirectory,sourcefile,self.repository))
    
    def GetSecondLineOfStampRecipe(self,sourcefile,sourcefilenumber):
        return str("	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/max/Projects/testcpp/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_{}) \"Formatting /home/max/Projects/testcpp/main.cpp and stamping it with /home/max/Projects/testcpp/build/main.cpp.stamp\"".format(sourcefilenumber))
    
    def GetCMakeFilesFormatContent(self,sourcefiles=list()):
        """This is the first block of the dynamically-written part of the build.make rule
        it produces ouptut like 
        CMakeFiles/format: foobar.cpp.stamp
        """
        content=list()
        for sourcefile in sourcefiles:
            content.append("CMakeFiles/format: "+sourcefile+".stamp")
        return content
    
    def WriteMakeFileOfFormattingRule(self):
        """This is the main function that will actually write the build.make for the formatting rule"""
        rule_make_file_list=[builddirectory,"CMakeFiles","format.dir","build.make"]
        code_generation_directory=os.sep.join(["cmake_modules","scripts"])
        self.DumpFileIntoOutputFile(os.sep.join([code_generation_directory,"format_rules_header.in"]),os.sep.join(rule_make_file_list),None,'w')

        self.DumpFileIntoOutputFile(os.sep.join([code_generation_directory,"format_rules_footer.in"]),os.sep.join(rule_make_file_list),None,'a')
        
        
    def DumpArrayOfLinesIntoOutputFile(self,content,outputfile,replacementdict=None,append_or_write="w"):
        with codecs.open(outputfile, append_or_write , encoding ='utf_8' ) as file:		#use a instead of w to append a+ to append/create w+ for write/create        
            file.write('\n'.join(content))

    def DumpFileIntoOutputFile(self,inputfile,outputfile,replacementdict=None,append_or_write="w"):
        content = [line.rstrip('\n') for line in open(inputfile)]
        self.DumpArrayOfLinesIntoOutputFile(content,outputfile,None,append_or_write)

def AsbolutePathToSourceFile(absolute_build_path,sourcefile,repository):
    """TODO delete me"""
    if os.path.isabs(sourcefile):
        return os.path.normpath(sourcefile)
    if os.path.isabs(repository):
        return os.path.normpath(os.sep.join([repository,sourcefile]))
    return ""



def GetCommandContentForStamp(sourcefile):
    content=list()
    return content
    
    
def GetCMakeFilesFormatContent(sourcefiles=list()):
    """TODO delete me """
    content=list()
    for sourcefile in sourcefiles:
        content.append("CMakeFiles/format: "+sourcefile+".stamp")
    return content


def main(argv):
    builddirectory=sys.argv[1]
    #relevant_file_extensions=sys.argv[2]
    
    print("Generating Format rule in {}".format(builddirectory))
    print(os.getcwd())

    relevant_source_files=list()
    files=glob.glob("**",recursive=True)
    for filepath in files:
        for extension in relevant_file_extensions.split(';'):
            if filepath.split('.')[-1]==extension.replace('.','') and not str(builddirectory+os.sep) in filepath :
                relevant_source_files.append(filepath)
                

    
    
    DumpArrayOfLinesIntoOutputFile(GetCMakeFilesFormatContent(relevant_source_files),os.sep.join(rule_make_file_list),None,'a')
    
        
    
    
#if __name__ == "__main__":
    #main(sys.argv)
