#! /usr/sh

cputemperature=$(bc<<<"scale=3;$(cat /sys/class/thermal/thermal_zone0/temp)/1000")
echo -e "CPU temperature is now: \e[41m$cputemperature\e[0m ℃"