#!/bin/bash 
set -euxo pipefail
DEBIAN_FRONTEND=noninteractive
sudo apt-get update
sudo apt-get install -y curl nano cmake gcc gcovr python3 python3-pip git texlive-full biber

python3 -m pip install -r requirements.txt

type -p curl >/dev/null || (sudo apt update && sudo apt install curl -y)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg 
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null 
sudo apt update
sudo apt install gh -y

rm -rf /var/lib/apt/lists/*
