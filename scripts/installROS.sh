#!/bin/bash

# Add sources.list
sudo sh -c '. /etc/lsb-release && echo "deb http://mirrors.tuna.tsinghua.edu.cn/ros/ubuntu/ `lsb_release -cs` main" > /etc/apt/sources.list.d/ros-latest.list'

sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

sudo apt-get update

sudo apt-get install -y ros-melodic-desktop-full

sudo apt install -y python-rosdep python-rosinstall python-rosinstall-generator python-wstool build-essential

sudo rosdep init
rosdep update

source /opt/ros/melodic/setup.bash
