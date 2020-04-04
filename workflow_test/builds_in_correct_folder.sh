#!/bin/bash
set -e
cd ..
TMP=$(mktemp -d)
cp -r project $TMP
cd $TMP 
cd project
./build.sh

if [ "$(ls -A build)" ] 
then 
    echo "Build directory is not empty. Good" 
else
    echo "build folder was empty. build.sh did not build in correct build directory" 
    exit 1
fi
