#!/bin/bash
./bin/testexe o
if [[ $? != "0" ]] ; then exit 1; fi
./bin/test_gtest_based --gtest_filter=This*
if [[ $? != "0" ]] ; then exit 1; fi
