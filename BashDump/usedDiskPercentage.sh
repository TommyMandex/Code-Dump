#!/bin/bash
#################################################################################
# ActiveXperts Network Monitor - Shell script checks
#
# For more information about ActiveXperts Network Monitor and SSH, please
# visit the online ActiveXperts Network Monitor Shell Script Guidelines at:
#   http://www.activexperts.com/support/network-monitor/online/linux/
#################################################################################
# Script
#     disk-used-pct.sh
# Description
#     Checks the used space on a disk
# Declare Parameters
#     1) sDrive (string) - Mounted drive
#     2) nMaxUsedPct (number) - Maximum used space (percentage)
# Usage
#     disk-used-pct.sh sDrive nMaxUsedPct
# Sample
#     bash ./disk-used-pct.sh /dev/sda1 90
#################################################################################

# This script is based on the 'df' command
# df -T output is like this:
# Filesystem     Type     1K-blocks    Used Available Use% Mounted on
# udev           devtmpfs   2001860       0   2001860   0% /dev
# tmpfs          tmpfs       403844   26368    377476   7% /run
# /dev/sda1      ext4     126820132 3797080 116557928   4% /
# tmpfs          tmpfs      2019208     156   2019052   1% /dev/shm
# tmpfs          tmpfs         5120       0      5120   0% /run/lock
# tmpfs          tmpfs      2019208       0   2019208   0% /sys/fs/cgroup
# cgmfs          tmpfs          100       0       100   0% /run/cgmanager/fs
# tmpfs          tmpfs       403844      64    403780   1% /run/user/1000


sDrive=$1
nMaxUsedPct=$2

# Validate number of arguments
if [ $# -ne 2 ] ; then
  echo "UNCERTAIN: Invalid number of arguments - Usage: disk-used-pct sDrive nMaxUsedPct"
  exit 1
fi

# Validate numeric parameter nMaxUsedPct
regExpNumber='^[0-9]+$'
if ! [[ $2 =~ $regExpNumber ]] ; then
  echo "UNCERTAIN: Invalid argument: nMaxUsedPct (number expected)"
  exit 1
fi

# Validate percentage - must be between 0 and 100
if [ $2 -lt 0 ] || [ $2 -gt 100 ] ; then
  echo "UNCERTAIN: Invalid argument $2 - Usage: disk-used-pct  "
  exit 1
fi

# Execute a command like this (assuming /dev/sda1). Note that slashes need to be escaped in AWK:
# df -T | awk '/\/dev\/sda1/ { print $6; }'
sDriveEsc=`echo $sDrive | sed 's/\//\\\\\//g'`        # e.g.: "\/dev\/sda1" <- "/dev/sda1"
sCommand="df -T | awk '/$sDriveEsc/ { print \$6; }'"  # e.g.: df -T | awk '/\/dev\/sda1/ { print $6; }'

# Get number of used pct
nPctUsed=`eval $sCommand`                             # e.g.: 4%
if [ -z "$nPctUsed" ]; then
  echo "UNCERTAIN: Drive [$sDrive] does not exist"
  exit 1
fi
nPctUsed=`echo $nPctUsed | sed 's/\%//g'`             # e.g.: 4

# Print final result. ActiveXperts will interpret the line, expected format is like this:
# [SUCCESS|ERROR|UNCERTAIN]  DATA:[]
if [ $nPctUsed -le $nMaxUsedPct ] ; then
  echo "SUCCESS: Free disk space on drive $sDrive=[$nPctUsed%], maximum allowed=[$nMaxUsedPct%] DATA:$nPctUsed"
else
  echo "ERROR: Free disk space on drive $sDrive=[$nPctUsed%], maximum allowed=[$nMaxUsedPct%] DATA:$nPctUsed"
fi	

# Exit script
exit 0
