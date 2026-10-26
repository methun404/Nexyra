#!/bin/bash
CPU=$(top -l 1 | grep "CPU usage" | awk '{print $3}' | tr -d '%')
RAM_TOTAL=$(sysctl -n hw.memsize | awk '{print $0/1024/1024/1024 " GB"}')
RAM_USED=$(top -l 1 | grep "PhysMem" | awk '{print $2}')

# Disk Info for Boot Drive (/)
# $2=Total, $3=Used, $5=Capacity
DISK_INFO=$(df -h / | tail -1)
DISK_TOTAL=$(echo "$DISK_INFO" | awk '{print $2}')
DISK_USED=$(echo "$DISK_INFO" | awk '{print $3}')
DISK_PCT=$(echo "$DISK_INFO" | awk '{print $5}' | tr -d '%')

echo "${CPU},${RAM_USED},${RAM_TOTAL},${DISK_USED},${DISK_TOTAL},${DISK_PCT}"
