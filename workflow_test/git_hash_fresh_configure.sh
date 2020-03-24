#!/bin/bash
set -e
cd ..
TMP=$(mktemp -d)
cp -r project $TMP
cd $TMP 
cd project
./build.sh
if [[ ! -f "version.hpp" ]]
then
    echo "Could not find version.hpp"
    exit 1
fi
version=$(cat "version.hpp" |grep "#define VERSION" | sed 's/#define VERSION//g' |sed 's/[[:space:]]//g')

if [ -z "$version" ] 
then
    echo "Version number is empty in version.hpp"
    exit 2 
fi

