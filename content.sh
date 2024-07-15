#!/bin/bash

# Directory to list files from
DIRECTORY=$1

# Check if directory is provided
if [ -z "$DIRECTORY" ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Check if the provided argument is a directory
if [ ! -d "$DIRECTORY" ]; then
    echo "Error: $DIRECTORY is not a directory."
    exit 1
fi

# List all files and their content recursively, excluding hidden files
find "$DIRECTORY" -type f -not -path '*/\.*' | while read -r FILE; do
    echo "File: $FILE"
    echo "Content:"
    cat "$FILE"
    echo ""
done
