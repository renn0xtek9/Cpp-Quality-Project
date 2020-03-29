SET (CMAKE_SYSTEM_NAME Linux)
SET (CMAKE_SYSTEM_PROCESSOR arm)

SET (
  CMAKE_SYSROOT
  ${CMAKE_SOURCE_DIR}/third-party/raspberrypitools/arm-bcm2708/arm-rpi-4.9.3-linux-gnueabihf/arm-linux-gnueabihf/sysroot/
)
# TODO should I define this ? SET (CMAKE_STAGING_PREFIX /home/devel/stage)

SET (
  CMAKE_C_COMPILER
  ${CMAKE_SOURCE_DIR}/third-party/raspberrypitools/arm-bcm2708/arm-rpi-4.9.3-linux-gnueabihf/bin/arm-linux-gnueabihf-gcc
)
SET (
  CMAKE_CXX_COMPILER
  ${CMAKE_SOURCE_DIR}/third-party/raspberrypitools/arm-bcm2708/arm-rpi-4.9.3-linux-gnueabihf/bin/arm-linux-gnueabihf-g++
)

SET (CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
SET (CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
SET (CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
SET (CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

ADD_DEFINITIONS (-Wall -std=c11)
