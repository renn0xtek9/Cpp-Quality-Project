#!/bin/bash 
sudo apt install googlest
cd /usr/src/googletest
sudo cmake  -DBUILD_SHARED_LIBS=ON CMakeLists.txt
sudo make
sudo make install

sudo apt install clang-format clang-tidy

pip3 install --user cmake-format


