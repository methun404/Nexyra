#!/bin/bash
TARGET_DIR=$1
if [ -z "$TARGET_DIR" ]; then
  echo "Error: No directory provided"
  exit 1
fi

# Ensure target subdirectories exist
mkdir -p "$TARGET_DIR/Images" "$TARGET_DIR/Documents" "$TARGET_DIR/Archives" "$TARGET_DIR/Videos"

# Smart move logic (case insensitive)
shopt -s nocaseglob

# Move images
mv "$TARGET_DIR"/*.{jpg,jpeg,png,gif,bmp,svg} "$TARGET_DIR/Images/" 2>/dev/null
# Move documents
mv "$TARGET_DIR"/*.{pdf,doc,docx,txt,xlsx,ppt,pptx} "$TARGET_DIR/Documents/" 2>/dev/null
# Move archives
mv "$TARGET_DIR"/*.{zip,tar,gz,rar,7z} "$TARGET_DIR/Archives/" 2>/dev/null
# Move videos
mv "$TARGET_DIR"/*.{mp4,mov,avi,mkv} "$TARGET_DIR/Videos/" 2>/dev/null

echo "Organization complete in $TARGET_DIR"
