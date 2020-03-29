#!/bin/bash
versionfile="build/debug-x86_64/version.hpp"
function CheckThatVersionHPPExistAndIsGood()
{
    if [[ ! -f "$versionfile" ]]
    then
        echo "Could not find $versionfile"
        exit 1
    fi
    version=$(cat $versionfile |grep "#define VERSION" | sed 's/#define VERSION//g' |sed 's/[[:space:]]//g')
    if [ -z "$version" ] 
    then
        echo "Version number is empty in $versionfile"
        exit 2 
    fi
    SHORT_HASH=$(git rev-parse --short HEAD)
    if [ "$version" != "$SHORT_HASH" ] 
    then 
        echo "VERSION in $versionfile: $version while SHORT_HASH: $SHORT_HASH"
        exit 3
    fi
}


set -e
cd ..
TMP=$(mktemp -d)
cp -r project $TMP
cd $TMP 
cd project

#init the git repo and make a first commit
git init 
git add * 
git commit -m "First Commit"

#Noe configure and build 
./build.sh

CheckThatVersionHPPExistAndIsGood


echo "// new comment" >>main.cpp
git add main.cpp
git commit -m "Second commit"
./build.sh

CheckThatVersionHPPExistAndIsGood


