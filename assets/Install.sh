#!/bin/bash

echo "Running installer for the Vimba SDK. Checking ARCH..."

UNAME=$(uname -m)

if [ ${UNAME} = amd64 ] || [ ${UNAME} = x86_64 ]
then
    ARCH=x86
    echo "x86 architecture detected"

    dos2unix VimbaUSBTL_x86/Install.sh 
    source VimbaUSBTL_x86/Install.sh

    dos2unix VimbaUSBTL_x86/SetGenTLPath.sh
    source VimbaUSBTL_x86/SetGenTLPath.sh

elif [ ${UNAME} = aarch64 ]
then
    ARCH=arm
    echo "ARM architecture detected"

    dos2unix VimbaUSBTL_ARM/Install.sh
    source VimbaUSBTL_ARM/Install.sh
        
    dos2unix VimbaUSBTL_ARM/SetGenTLPath.sh
    source VimbaUSBTL_ARM/SetGenTLPath.sh

else
   echo "Error: Incompatible system architecture found." 1>&2
   exit 1
fi
