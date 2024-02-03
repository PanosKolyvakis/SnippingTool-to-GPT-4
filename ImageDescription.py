import tkinter as tk
from PIL import Image, ImageTk
import base64
import requests
import os
from Config import PathConfig 
import subprocess

path_config = PathConfig()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def ImDescribe(prompt='Describe this picture'):
    image_path = path_config.screenshot_path
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {path_config.api_key}"
    }


    payload = {
        "prompt": prompt,
        "image": base64_image, 
        "max_tokens": 300
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
            response_data = response.json()
            output_text = response_data.get('choices', [{}])[0].get('message', {}).get('content', "Response content not found")
        else:
            output_text = f"Error: {response.status_code}\n{response.text}"
    except Exception as e:
        output_text = f"An error occurred: {e}"

    with open(path_config.api_output_path, 'w') as file:
        file.write(output_text)
    return output_text

def read_description_aloud():
    # Assuming description_label is globally defined and updated elsewhere
    description = description_label.cget("text")
    voice = "Tessa"
    subprocess.run(['say', '-v', voice, description])

def display_gui(image_path, description):
    global description_label
    root = tk.Tk()
    root.title("Image and Description")

    # Load and display the image
    img = Image.open(image_path)
    max_size = 500
    original_width, original_height = img.size
    ratio = min(max_size/original_width, max_size/original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    img_photo = ImageTk.PhotoImage(img)
    panel = tk.Label(root, image=img_photo)
    panel.pack(side="top", fill="both", expand="yes")

    # Display the description
    description_label = tk.Label(root, text=description, wraplength=500)
    description_label.pack(side="bottom", fill="x", expand="yes")


    read_button = tk.Button(root, text="Read Description", command=lambda: read_description_aloud())
    read_button.pack(side="bottom")

    root.mainloop()

if __name__ == '__main__':
    image_path = path_config.screenshot_path
    description = ImDescribe() 
    display_gui(image_path, description)
