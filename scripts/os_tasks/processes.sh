#!/bin/bash
# Using 'ps' to get PID, Command, %CPU, and %MEM
# We use 'ps -eo' and set a custom format to avoid truncation and use commas as separators carefully
# On macOS, 'comm' usually contains the full path or truncated name
ps -eo pid,pcpu,pmem,comm -m | awk 'NR>1 {
    # $1 is PID, $2 is CPU, $3 is MEM, $4... is COMM
    pid=$1; cpu=$2; mem=$3;
    comm=""; for(i=4;i<=NF;i++) comm=comm $i " ";
    print pid "," comm "," cpu "," mem
}' | head -n 30
