#!/bin/sh
# Author: Mikoy Chinese
# This script will auto reload or reset the usb connectting.
# It will creat a application in /tmp/ and creat a C code file.

#debug=$(lsusb)

Bus=($(lsusb | awk '{print substr($2,1,3)}'))
Device=($(lsusb | awk '{print substr($4,1,3)}'))

# C code file.
echo "/* usbreset -- send a USB port reset to a USB device */

#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/ioctl.h>

#include <linux/usbdevice_fs.h>


int main(int argc, char **argv)
{
    const char *filename;
    int fd;
    int rc;

    if (argc != 2) {
        return 1;
    }
    filename = argv[1];

    fd = open(filename, O_WRONLY);
    if (fd < 0) {
        return 1;
    }

    rc = ioctl(fd, USBDEVFS_RESET, 0);
    if (rc < 0) {
        return 1;
    }

    close(fd);
    return 0;
}" > /tmp/usbreset.c

$(cc /tmp/usbreset.c -o /tmp/usbreset)
$(chmod +x /tmp/usbreset)

for((i=0;i<${#Bus[*]};i++))
do
    $(cd /tmp/;./usbreset /dev/bus/usb/${Bus[$i]}/${Device[$i]})
    result=$?
    keyword=($(lsusb -s ${Bus[$i]}:${Device[$i]}))
    if [ $result != 0 ];then
        echo "-------------------Reset Usb Failed!--------------------------------"
        echo "Please make sure it's right: $keyword"
    else
        echo "Reset Usb <<$keyword>> Successfully!"
    fi
done
