# import statements

import pytesseract
from PIL import Image
import openai
from gui import run_gui

def process_image_with_prompt(image_path, prompt):
    # Replace 'your_api_key' with your OpenAI API key
    openai.api_key = 'your_api_key'
    image = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(image)

    prompt_text = f"The following text was extracted from a question: {extracted_text}. {prompt}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "check prompt"},
                {"role": "user", "content": prompt_text}
            ]
        )
        return response['choices'][0]['message']['content'] if response['choices'][0]['message'] else "No content received from API."
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    selected_prompt = run_gui()
    output_text = process_image_with_prompt('path_to_your_image.png', selected_prompt)

    # Replace 'output.txt' with the desired output file path
    with open('output.txt', 'w') as file:
        file.write(output_text)



