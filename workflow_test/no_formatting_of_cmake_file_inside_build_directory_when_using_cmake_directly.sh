#!/bin/bash
set -e
cd ..
TMP=$(mktemp -d)
cp -r project $TMP
cd $TMP 
cd project
mkdir -p build 
cd build 
cmake -DCMAKE_BUILD_TYPE=Debug ..  > build.log

number_of_files_under_build=$(cat build.log  |grep Formatting: |grep project/build |wc -l)
if [[ $number_of_files_under_build == "0" ]]
then 
    exit 0
else 
    exit 1
fi
