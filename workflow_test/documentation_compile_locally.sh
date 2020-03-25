#!/bin/bash
set -e
cd ..
TMP=$(mktemp -d)
cp -r project $TMP
cd $TMP 
cd project
mkdir -p build
cd build 
cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Debug ..
echo "Will make documentation"
make software-intern-development
if [[ ! -f "documentation/software-intern-development.pdf" ]]
then
    echo "Could not find build/documentation/software-intern-development.pdf"
    exit 1
fi
