#!/usr/bin/env bash

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

shell_folder="shell"

files=("$shell_folder"/*)

for file_path in "${files[@]}"; do
    file_name=$(basename "$file_path")

    if command_exists "$file_name"; then
        echo "Skipping $file_name - Command already exists"
    else
        chmod u+x "$file_path"
        echo "$file_name is executable"
        cp $file_path /usr/local/bin
        echo "$file_name moved"
    fi
done