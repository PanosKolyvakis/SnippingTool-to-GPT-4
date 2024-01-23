#!/bin/zsh

# Add Conda to PATH
# Assuming Conda is installed in a standard location that's already in the PATH
export PATH="$HOME/miniconda3/bin:$PATH"

# Activate your Conda environment
# It's better to activate conda by initializing in .zshrc or .bashrc
# This line is here just in case it's not initialized
source "$HOME/miniconda3/etc/profile.d/conda.sh" || echo "Error: Conda not found. Please make sure it's installed and added to your PATH."
conda activate ImageToText || echo "Error: Failed to activate Conda environment 'ImageToText'."

# Define screenshot directory and filenames
screenshot_directory="$HOME/VSprojects/ImageToText"
screenshot_filename="screenshot.png"
output_filename="output.txt"

# Create the directory if it doesn't exist
mkdir -p "$screenshot_directory"

# Capture the screenshot
screencapture -i -t png "$screenshot_directory/$screenshot_filename"

# Check if the user canceled or captured the screenshot
if [ $? -eq 0 ]; then
    echo "Screenshot saved successfully."

    # Call your Python script to process the screenshot
    # Assuming the script is in the same directory as the screenshot
    python3 "$screenshot_directory/main.py" > "$screenshot_directory/$output_filename" || echo "Error: Failed to run the script 'main.py'."
	python3 "$screenshot_directory/IDE.py" || echo "Error: Failed to run the script 'IDE.py'."
else
    echo "Screenshot capture canceled."
fi
