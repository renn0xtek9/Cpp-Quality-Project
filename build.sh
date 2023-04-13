#!/bin/bash 
set -e 
rm -rf build
mkdir -p build
cd build 
# conan install ../conanfile.txt -pr ./../conan_profiles/linux-x86 --build missing
conan install ../conanfile.txt --profile:build=../conan_profiles/linux-x86 --profile:host=../conan_profiles/linux-x86 --build missing
cmake ..
make 
make test
