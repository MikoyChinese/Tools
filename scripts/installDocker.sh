#!/bin/bash

# This script help you install docker by ustc mirrors automatically.

# Uninstall old versions.
sudo apt-get remove docker docker-engine docker.io containerd runc

# Update the apt package index and install dependence.:
sudo apt-get update
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
    
# Add Docker's official GPG key:
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Set up the stable repository for ustc docker mirrors repository.
sudo add-apt-repository \
   "deb [arch=amd64] https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
   
# Install Docker CE
sudo apt-get update
# For the lastest version. If you wanna to install special version, such like following:
# Example: sudo apt-get install docker-ce=<VERSION_STRING> docker-ce-cli=<VERSION_STRING> containerd.io
# List all the version available in your repo: apt-cache madison docker-ce
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Verify that Docker Ce:
sudo docker run hello-world
sudo gpasswd -a ${USER} docker
sudo service docker restart
newgrp - docker
