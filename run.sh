#!/bin/bash

# Set the folder containing Python files (default to current directory)
FOLDER=${1:-.}

# Find and execute all Python files in the folder
for file in "$FOLDER"/*.py; do
    if [ -f "$file" ]; then
        echo "Running: $file"
        python "$file"
        echo "Finished: $file"
        echo "-------------------------"
    fi
done
