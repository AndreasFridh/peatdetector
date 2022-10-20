#!/bin/bash

echo "Running installer"

UNAME=$(uname -m)

if [ ${UNAME} = amd64 ] || [ ${UNAME} = x86_64 ]
then
    ARCH=x86
    echo "x86 architecture detected"
    dos2unix VimbaUSBTL_x86/Install.sh 
    source VimbaUSBTL_x86/Install.sh

elif [ ${UNAME} = aarch64 ]
then
    ARCH=arm
    echo "ARM architecture detected"
    dos2unix VimbaUSBTL_x86/Install.sh
    source VimbaUSBTL_ARM/Install.sh

else
   echo "Error: Incompatible system architecture found." 1>&2
   exit 1
fi
