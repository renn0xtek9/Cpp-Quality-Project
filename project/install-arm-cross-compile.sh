#!/bin/bash
set -e 
mkdir -p third-party/raspberrypitools
cd third-party/

rm -rf raspberrypitools
git clone https://github.com/raspberrypi/tools raspberrypitools

rm -rf wiringPi
git clone https://github.com/WiringPi/WiringPi wiringPi

sudo apt install g++-arm-linux-gnueabihf gcc-arm-linux-gnueabihf -y
