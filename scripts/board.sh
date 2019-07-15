#!/bin/bash
#------------------------------------------------#
# This script is for the pre-install of the board#
#------------------------------------------------#
##################################################
#  Usage: ./board.sh                             #
# Author: Mikoy Chinese                          # 
#   Date:   2019-06-28                           # 
#  Email: mikoychinese@gmail.com                 #
##################################################

# Font color.
RED='\033[0;31m'
GREEN='\033[0;32m'
PLAIN='\033[0m'

# Be sure as root.
[[ $EUID -ne 0 ]] && echo -e " ${RED}Error:${PLAIN} This script must be run as root!" && exit 1

# Get your release.
release=$(lsb_release -c -s)

# Install apt-transport-https.
echo -e "${GREEN}Install apt-transport-https.\n${PLAIN}"
sudo apt-get install apt-transport-https -y

# Replace the apt sources.list
echo -e "${GREEN}Replace the apt sources.list.\n${PLAIN}"
if [[ -f /etc/apt/sources.list.bak ]]; then
    echo -e " ${GREEN}sources.list.bak exists${PLAIN}"
else
    mv /etc/apt/sources.list{,.bak}
fi

[ -f /etc/apt/sources.list ] && rm /etc/apt/sources.list

echo "deb https://mirrors.ustc.edu.cn/ubuntu/ $release main restricted universe multiverse" >> /etc/apt/sources.list
echo "deb-src https://mirrors.ustc.edu.cn/ubuntu/ $release main restricted universe multiverse" >> /etc/apt/sources.list
echo -e "\n" >> /etc/apt/sources.list
echo "deb https://mirrors.ustc.edu.cn/ubuntu/ $release-security main restricted universe multiverse" >> /etc/apt/sources.list
echo "deb-src https://mirrors.ustc.edu.cn/ubuntu/ $release-security main restricted universe multiverse" >> /etc/apt/sources.list
echo -e "\n" >> /etc/apt/sources.list
echo "deb https://mirrors.ustc.edu.cn/ubuntu/ $release-updates main restricted universe multiverse" >> /etc/apt/sources.list
echo "deb-src https://mirrors.ustc.edu.cn/ubuntu/ $release-updates main restricted universe multiverse" >> /etc/apt/sources.list
echo -e "\n" >> /etc/apt/sources.list
echo "deb https://mirrors.ustc.edu.cn/ubuntu/ $release-backports main restricted universe multiverse" >> /etc/apt/sources.list
echo "deb-src https://mirrors.ustc.edu.cn/ubuntu/ $release-backports main restricted universe multiverse" >> /etc/apt/sources.list
echo -e "\n## Not recommended" >> /etc/apt/sources.list
echo "# deb https://mirrors.ustc.edu.cn/ubuntu/ $release-proposed main restricted universe multiverse" >> /etc/apt/sources.list
echo "# deb-src https://mirrors.ustc.edu.cn/ubuntu/ $release-proposed main restricted universe multiverse" >> /etc/apt/sources.list

apt-get update

# Install openssh-server.
echo -e "${GREEN}Install openssh-server.\n${PLAIN}"
sudo apt-get install openssh-server -y



echo -e "${GREEN}Done${PLAIN}"
# Install xrdp vnc4server xbase-clients dconf-editor.
#echo
#echo -e "Install xrdp vnc4server xbase-clients dconf-editor.\n"
#sudo apt-get install xrdp vnc4server xbase-clients dconf-editor -y

# Edit the org.gnome.Vino setting.
#echo
#echo -e "Edit the org.gnome.Vino setting.\n"
#sudo gsettings set org.gnome.Vino require-encryption false
