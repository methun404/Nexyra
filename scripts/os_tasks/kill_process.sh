#!/bin/bash
PID=$1
if [ -n "$PID" ]; then
    kill -9 "$PID"
    echo "Success"
else
    echo "Error: No PID provided"
fi
