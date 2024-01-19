#!/bin/zsh

# Add Conda to PATH (the user needs to replace the placeholder with the actual path to their Conda bin directory)
export PATH="/path/to/conda/bin:$PATH"

# Source the Conda configuration (the user needs to replace the placeholder with the actual path to their conda.sh)
source /path/to/conda/etc/profile.d/conda.sh
# Activate the Conda environment (the user should replace 'your_env' with the name of their Conda environment)
conda activate your_env

# Set the directory where you want to save the screenshot and output file
# The user should replace these placeholders with the paths where they want to save screenshots and outputs
screenshot_directory="path/to/directory/for/screenshot"
screenshot_filename="screenshot.png"
output_filename="output.txt"

# Take a screenshot and save it to the specified directory
screencapture -i -t png "$screenshot_directory/$screenshot_filename"

# Check if the user canceled or captured the screenshot
if [ $? -eq 0 ]; then
    echo "Screenshot saved successfully."

    # Call the Python script to process the screenshot
    # The user should replace 'path/to/python/script' with the path to their Python script
    python3 path/to/python/script/main.py > "$screenshot_directory/$output_filename"
    
    # Open the output text file in TextEdit or any other preferred text editor
    open -a TextEdit "$screenshot_directory/$output_filename"
else
    echo "Screenshot capture canceled."
fi
