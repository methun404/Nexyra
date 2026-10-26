#!/bin/bash
TARGET="test_workspace"
mkdir -p "$TARGET"
touch "$TARGET/report.pdf" "$TARGET/notes.txt" "$TARGET/script.py" "$TARGET/photo.jpg" "$TARGET/logo.png" "$TARGET/video.mp4"
echo "This is garbage data" > "$TARGET/temp_001.tmp"
echo "More garbage" > "$TARGET/temp_002.log"
mkdir -p "$TARGET/old_cache"
touch "$TARGET/old_cache/data.bin"
echo "Workspace populated for demo."
