#!/bin/bash
TARGET_DIR=$1
if [ -z "$TARGET_DIR" ]; then
  echo "Error: No directory provided"
  exit 1
fi

# We only clear specific safe junk in real system paths
# For ~/Library/Caches and ~/Library/Logs
if [[ "$TARGET_DIR" == *"Library/Caches"* || "$TARGET_DIR" == *"Library/Logs"* ]]; then
    # Clear subdirectories and files
    find "$TARGET_DIR" -mindepth 1 -maxdepth 2 -delete 2>/dev/null
    echo "Cleared $TARGET_DIR"
else
    # Safety fallback for other directories (test workspaces)
    rm -rf "$TARGET_DIR"/*.tmp 2>/dev/null
    rm -rf "$TARGET_DIR"/*.log 2>/dev/null
    echo "Cleaned $TARGET_DIR"
fi
