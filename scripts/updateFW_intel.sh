#!/bin/bash
# This shell file is for updating realsense sensor Firmware. And support for multi realsensen cameras update together.
# Usage: ./updateFw_intel.sh [Firmware bin]
# The lastest Firmware bin file downloads from https://realsense.intel.cn/intel-realsense-downloads/
#
# System: Ubuntu16 or Ubuntu18
# 
# Author: Mikoy Chinese
#   Date: 2019-03-20
# Github: https://github.com/mikoychinese 

if [ $# -ne 1 ]
then
    echo "Useage: $0 [Firmware bin]"
    echo "Help: $0 -h"
    exit 1
fi

if [ ! -x "/bin/intel-realsense-dfu" ];then
    echo "$0: [intel-realsense-dfu] No Found in local machine."
    read -n1 -t 30 -p "Do you want to install intel-realsense-dfu? [y/N]" answer
    echo
    case $answer in
    Y | y)
    	release=$( (lsb_release -a)|awk '{print $2}'|tail -n 1 )
        apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key C8B3A55A6F3EFCDE
        add-apt-repository "deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo $release main" -u
        apt-get update
        apt-get install intel-realsense-dfu*
    ;;
    *)
        exit 1
    ;;
    esac
fi

case $1 in
    -h | --help)
        echo "Useage: $0 [Firmware bin]"
        echo "The lastest Firmware bin file downloads from https://realsense.intel.cn/intel-realsense-downloads/."
    ;;
    
    *)
    	echo "================================="
    	echo "----- AUTHOR: Mikoy Chinese -----"
    	echo "-----    INTEL REALSENSE    -----"
        bus=(`lsusb | grep Intel | awk '{print $2}'`)
        device=(`lsusb | grep Intel | awk '{print $4}' | cut -c 1-3`)
        fw_file=$1
        for i in `seq ${#bus[@]}`
        do
        	{
        		echo "[UPDATE FIRMWARE]>>> Bus: ${bus[i-1]} Device: ${device[i-1]}"
        		/bin/intel-realsense-dfu -b ${bus[i-1]} -d ${device[i-1]} -f -i $fw_file
        		echo ""
        		echo "======================================="
        	} || {
        		echo "[SKIP]>>> Bus: ${bus[i-1]} Device: ${device[i-1]}"
        		echo ""
        		echo "======================================="
        		continue
        	}
        done
	;;
esac
