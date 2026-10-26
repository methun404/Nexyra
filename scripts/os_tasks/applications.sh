#!/bin/bash
# List all .app directories in /Applications with their full paths
find /Applications -maxdepth 1 -name "*.app" | head -n 40
