#!/bin/zsh


# Add Conda to PATH
export PATH="/Users/panoskolyvakis/opt/miniconda3/bin:/opt/homebrew/bin:$PATH"



# Activate your Conda environment
source /Users/panoskolyvakis/opt/miniconda3/etc/profile.d/conda.sh
conda activate ImageToText

screenshot_directory="/Users/panoskolyvakis/VSprojects/ImageToText"
screenshot_filename="screenshot.png"
screencapture -i -t png "$screenshot_directory/$screenshot_filename"
output_filename="output.txt" 

# Check if the user canceled or captured the screenshot
if [ $? -eq 0 ]; then
    echo "Screenshot saved successfully."

    # Call your Python script to process the screenshot
    python3 /Users/panoskolyvakis/VSprojects/ImageToText/main.py > "$screenshot_directory/$output_filename"
	open -a TextEdit "$screenshot_directory/$output_filename"
else
    echo "Screenshot capture canceled."
fi
