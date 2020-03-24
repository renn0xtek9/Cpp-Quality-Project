#!/bin/bash 
mkdir -p build
cmake -G "Unix Makefiles" --build build -DCMAKE_BUILD_TYPE=Debug .
make 
