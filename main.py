# import statements 
import pytesseract
from PIL import Image
import  openai

openai.api_key='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'


path = '/Users/panoskolyvakis/VSprojects/ImageToText/screenshot.png'
# Load an image
image = Image.open(path)

# Use Tesseract to do OCR on the image
extracted_text = pytesseract.image_to_string(image)

prompt_text= f'The following text was extracted from an image: {extracted_text}. Can you explain what this means? if it is a paragraph provide a small easy-to-understand overview. If it is a question please answer it. If it looks like a SQL or programming question please write code to solve it'

try:
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": prompt_text}
      ]
    )
    output_text = response['choices'][0]['message']['content'] if response['choices'][0]['message'] else "No content received from API."
except Exception as e:
    output_text = f"An error occurred: {e}"

# Write the output to a text file
with open('/Users/panoskolyvakis/VSprojects/ImageToText/output.txt', 'w') as file:
    file.write(output_text)



