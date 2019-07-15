#!/bin/bash
# Author: Mikoy Chinese Date: 2019-07-03
# This script will auto-send the images files to the special path.
# It will creat a folder on your PC
#------------------------------------------------------
# @REMOTE_HOST: The remote host you want to rsync the data.
# @   SSH_PORT: The ssh port, default is 22.
# @REMOTE_USER @PASSWORD: The user and pwd of the remote host.
# @ REMOTE_DIR: The Path where is the data you want to transport to your PC.
# @   SAVE_DIR: The path where you want to save.
#------------------------------------------------------
REMOTE_HOST=192.168.20.161                                                                           
SSH_PORT=22
REMOTE_USER="comma"
PASSWORD="123456"
REMOTE_DIR="/home/comma/software"
SAVE_DIR="/home/commaai-03/Test/tmp/tmp"

function Install_sshpass_rsync(){
    sshpass -V > /dev/null 2&>1
    if [ $? -ne 0 ]
    then
		echo "$0: Then command sshpass was not found."
		read -n1 -t 30 -p "Do you want to install sshpass? [y/N]" answer
		echo
		case $answer in
		Y | y)
			sudo apt-get install -y sshpass
			command -v rsync >/dev/null 2>&1 || { sudo apt-get install -y rsync; }
		;;
		*)
			exit 1
		;;
		esac
	fi
}

Install_sshpass_rsync

echo "======================================="
echo "         Start To Transport            "                                       
echo "======================================="
# ssh -c aes128-gcm@openssh.com see details from https://blog.famzah.net/2015/06/26/openssh-ciphers-performance-benchmark-update-2015/
sshpass -p "$PASSWORD" rsync -avzP --progress -e "ssh -c aes128-gcm@openssh.com -p $SSH_PORT" $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR $SAVE_DIR

if [ $? -eq 0 ]; then
	echo "======================================="
	echo "         Transport Completely          "
	echo "======================================="
fi
