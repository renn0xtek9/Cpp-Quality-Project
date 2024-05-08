#!/bin/bash 
set -euxo pipefail
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"/../
rm -rf build
mkdir -p build
cd build 
conan install ../conanfile.txt --profile:build=../conan_profiles/linux-x86 --profile:host=../conan_profiles/linux-x86 --build missing
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_EXPORT_COMPILE_COMMANDS=ON --graphviz=cmake.dot
