#!/bin/bash
./testexe o
if [[ $? != "0" ]] ; then exit 1; fi
./test_gtest_based --gtest_filter=This*
if [[ $? != "0" ]] ; then exit 1; fi
