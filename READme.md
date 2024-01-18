# Image to Text Automation Tool

## Overview
This project provides a convenient macOS Quick Action that captures a selected area of the screen, performs Optical 
Character Recognition (OCR) on the captured image, and then uses OpenAI's GPT-3.5-turbo model (or any other model they offer, you can use GPT-4 for best results) to interpret or answer 
questions based on the extracted text. The result is displayed in a text editor, providing a seamless workflow from image 
capture to text analysis.

## Features
- **Screen Capture**: Take a screenshot of a selected area using macOS's built-in screencapture utility.
- **Text Extraction**: Utilize Tesseract OCR to convert image content into plain text.
- **AI-Powered Analysis**: Leverage OpenAI's GPT-3.5-turbo to understand, explain, or answer the text extracted from the 
image.
- **User-Friendly Output**: Display the AI's response in a text file that opens automatically in TextEdit, offering a 
readable and convenient presentation of results.

## Prerequisites
- macOS with Automator
- Python 3 installed and accessible within a Conda environment
- Tesseract OCR installed (`brew install tesseract` using Homebrew)
- OpenAI API key with access to GPT-3.5-turbo

## Installation
Clone the repository and navigate to the downloaded directory:
```bash
git clone https://github.com/PanosKolyvakis/SmartCapture-Image-Text-Extraction-Analysis
cd SmartCapture-Image-Text-Extraction

## next steps
Get an API key from OpenAI and substitute in main.py the https://platform.openai.com/api-keys
Do not forget to change directory names as well in the main.py
Before running the script, update the following variables in the script to match your local environment:

- `screenshot_directory`: The path to the directory where you want to save screenshots.
- `output_filename`: The name of the file where you want to save the output text.


setting up your conda environment (it can be venv as well but i am using conda)
conda create EnvName
pip install -r requirements.txt
conda Activate

