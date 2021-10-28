#!/bin/bash
# Author: Mikoy Chinese | https://github.com/MikoyChinese
# Update geoip.dat and geosite.dat from https://github.com/Loyalsoldier/v2ray-rules-dat

Green_font_prefix="\033[32m"
Red_font_prefix="\033[31m"
Font_color_suffix="\033[0m"
INFO="${Green_font_prefix}[INFO]${Font_color_suffix}"
ERROR="${Red_font_prefix}[ERROR]${Font_color_suffix}"

download_dat(){
    file=$1
    url=$2
    if [ ! -f $file ];then
        echo -e "${INFO}:${file} is not existed. Downloading..."
	wget $url -O $file
    else
	echo "================================="
	echo "              $file              "
	echo "================================="
	echo -e "${INFO}: Move $file to back file."
	echo
	mv $file "${file}.bak"
	wget $url -O $file
	if [ "$?" -eq 0 ];then
	    rm -f "${file}.bak"
	    echo -e "${INFO}: Update successfully!"
	else
	    mv "${file}.bak" $file
	    echo -e "${ERROR}: Failed!"
	    exit 1
	fi
	
    fi
}

# Download the lastest date.

download_dat geoip.dat https://cdn.jsdelivr.net/gh/Loyalsoldier/v2ray-rules-dat@release/geoip.dat

download_dat geosite.dat https://cdn.jsdelivr.net/gh/Loyalsoldier/v2ray-rules-dat@release/geosite.dat
