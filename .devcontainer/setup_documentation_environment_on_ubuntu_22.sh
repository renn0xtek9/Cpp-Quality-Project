#!/bin/bash 
set -euxo pipefail
DEBIAN_FRONTEND=noninteractive
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"
sudo apt-get update
sudo apt-get install -y cmake git texlive-full biber doxygen graphviz makefile2graph
python3 -m pip install -r requirements.txt
