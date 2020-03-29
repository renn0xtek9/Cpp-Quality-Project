#!/bin/bash 
# mkdir -p build
# cd build
# cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Debug ..
# make -j 12
# 
# exit 0

#!/bin/bash
function FindToolchain ()
{
    script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    cd $script_dir
    toolchain=$(find -name "$1")
    echo $toolchain
}
Builds=("debug-x86_64" "debug-raspberry")
mkdir -p build && cd build 
for build in ${Builds[@]}
do 
    cmakecommand="cmake "
    if [[ $build == *"debug"* ]]; then   #eg if [[ $str == *"in"* ]]
        cmakecommand=$(echo $cmakecommand "-DCMAKE_BUILD_TYPE=Debug")
    fi
    architecture=$(echo $build |sed 's/.*-\(.*\)/\1/g') 
    if [[ "$architecture" != "$(uname -m)" ]] 
    then
        $toolchain=$(FindToolchain "toolchain-$architecture.cmake")
        cmakecommand=$(echo $cmakecommand "-DCMAKE_TOOLCHAIN_FILE=$toolchain")   
    fi 
    cmakecommand=$(echo $cmakecommand ./../../)
    mkdir -p $build 
    cd $build
    echo $cmakecommand    
    eval $cmakecommand 
    cd ..
    
done 


