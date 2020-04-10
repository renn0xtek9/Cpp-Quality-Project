#!/bin/bash
set -e
cd ..
TMP=$(mktemp -d)
cp -r project $TMP
cd $TMP 
cd project
rm -rf cmake_modules/scripts/generate_format_rules_tests/
./build.sh > build.log
cd build/debug-x86_64
make > make.log

number_of_files_under_build=$(cat make.log |grep Formatting |sed 's/\[ [0-9][0-9]%\] Formatting \(.*\) and stam.*/\1/g' |grep -v Formatting: |grep build |wc -l)
if [[ $number_of_files_under_build == "0" ]]
then 
    exit 0
else 
    echo "FAILED there was $number_of_files_under_build files formatted in the build directory"
    exit 1
fi
