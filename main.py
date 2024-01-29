# import statements

from PIL import Image
import openai
from gui import run_gui
from Config import PathConfig
from IDE import main_s
import pytesseract  

def process_image_with_ocr(image_path):
    image = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text

def get_response_from_openai_api(extracted_text, prompt, selected_model):
    openai.api_key = PathConfig.api_key
    prompt_text = f"The following text was extracted from a question: {extracted_text}. {prompt}"

    try:
        response = openai.ChatCompletion.create(
            model=selected_model,
            messages=[
                {"role": "system", "content": "check prompt"},
                {"role": "user", "content": prompt_text}
            ]
        )
        return response['choices'][0]['message']['content'] if response['choices'][0]['message'] else "No content received from API."
    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":

    PathConfig = PathConfig()
    
    extracted_text = process_image_with_ocr(PathConfig.screenshot_path)
    if extracted_text:

        # Write the extracted text to the OCR output path
        with open(PathConfig.ocr_output_path, 'w') as file:
            file.write(extracted_text)

        selected_prompt, selected_model = run_gui()

        if selected_prompt:
            output_text = get_response_from_openai_api(extracted_text, selected_prompt, selected_model)


            
        with open(PathConfig.api_output_path, 'w') as file:
            
            file.write(output_text)


        main_s()
    else:
        pass 
