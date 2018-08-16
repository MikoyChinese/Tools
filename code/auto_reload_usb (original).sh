#!/bin/sh
# Usage: ./resetusb ARGUMENT(The keyword for your usb device)

var1=$1
keyword=${var1:=Storage}

debug=$(lsusb)
bus=$(lsusb|grep $keyword|perl -nE "/\D+(\d+)\D+(\d+).+/; print qq(\$1)")
device=$(lsusb|grep $keyword|perl -nE "/\D+(\d+)\D+(\d+).+/; print qq(\$2)")

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
$(cd /tmp/;./usbreset /dev/bus/usb/$bus/$device)
result=$?
if [ $result != 0 ];then
    echo "Reset Usb Failed!"
    echo "Please make sure you have inputted right device keyword: $keyword"
    echo "You have chose bus:${bus:=Not Found},device:${device:=Not Found}"
    echo "More info:\n$debug"
else
    echo "Reset Usb $keyword Successfully!"
fi
