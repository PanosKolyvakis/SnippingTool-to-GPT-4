# import statements
import pytesseract
from PIL import Image
import openai
import os

# Retrieve the OpenAI API key from environment variables for better security
# Users must set this environment variable in their system before running the script
openai.api_key = os.getenv('OPENAI_API_KEY')

# Path where the screenshot is saved
# Users should update this path to where they want their screenshot to be saved
path = '/path/to/your/screenshot.png'  # TODO: Replace with your path

# Load an image
image = Image.open(path)

# Use Tesseract to do OCR on the image
extracted_text = pytesseract.image_to_string(image)

# Construct the prompt text with the extracted text
prompt_text= f'The following text was extracted from  a question: {extracted_text}.   This is a verbal reasoning test. Answer with only information received from the text. If there are what appears to be options (A , B ,C etc) then consider all answers equally and  give me the answer. For False or True the information has to be explicitely contained within the text otherwise choose Cannot Say'

# Try to get a response from OpenAI's API
try:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt_text}
        ]
    )
    # Extract the content from the response if available
    output_text = response['choices'][0]['message']['content'] if response['choices'][0]['message'] else "No content received from API."
except Exception as e:
    # Capture and write any exceptions to the output text
    output_text = f"An error occurred: {e}"

# Output file path
# Users should update this path to where they want their output to be saved
output_path = '/path/to/your/output.txt'  # TODO: Replace with your path

# Write the output to a text file
with open(output_path, 'w') as file:
    file.write(output_text)



