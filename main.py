from PIL import Image
import openai
from gui import run_gui
from Config import PathConfig
from IDE import main_s
import pytesseract  
from ImageDescription import ImDescribe , display_gui

path_config = PathConfig()

def process_image_with_ocr(image_path):
    image = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text if extracted_text else None

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
    vision_model = 'gpt-4-vision-preview'

    extracted_text = process_image_with_ocr(PathConfig.screenshot_path)
    extracted_text = extracted_text if extracted_text else ' '

    # Write the extracted text to the OCR output path
    with open(PathConfig.ocr_output_path, 'w') as file:
        file.write(extracted_text)

    # run the GUI for the prompt and model selection
    selected_prompt, selected_model = run_gui()
    
    # this code gets executed if 
    if selected_prompt and selected_model!= vision_model:

        output_text = get_response_from_openai_api(extracted_text, selected_prompt, selected_model)
        with open(PathConfig.api_output_path, 'w') as file:
        
            file.write(output_text)

        main_s()

    # this code gets executed if the Vision model is selected and it will generate a description of the image
    else:
        display_gui(path_config.screenshot_path, ImDescribe())
    


    

