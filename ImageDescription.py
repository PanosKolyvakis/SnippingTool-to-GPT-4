import tkinter as tk
from PIL import Image, ImageTk
import base64
import requests
from Config import PathConfig

# Assuming PathConfig is correctly set up and accessible
path_config = PathConfig()

def ImDescribe():
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    image_path = path_config.screenshot_path
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {path_config.api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What’s in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
            response_data = response.json()

            if response_data.get('choices') and response_data['choices'][0].get('message'):
                output_text = response_data['choices'][0]['message']['content']
            else:
                output_text = "Response content not found"
        else:
            output_text = f"Error: {response.status_code}\n{response.text}"

    except Exception as e:
        output_text = f"An error occurred: {e}"

    # with open(path_config.api_output_path, 'w') as file:
    #     file.write(output_text)
    return output_text

    # Displaying the image and the description in a Tkinter window
def display_gui(image_path, description):
    root = tk.Tk()
    root.title("Image and Description")

    # Load the image
    img = Image.open(image_path)

    # Calculate the scaling factor to maintain aspect ratio
    max_size = 500
    original_width, original_height = img.size
    ratio = min(max_size/original_width, max_size/original_height)

    # Compute new dimensions
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)

    # Resize the image
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    img_photo = ImageTk.PhotoImage(img)

    # Display the image
    panel = tk.Label(root, image=img_photo)
    panel.pack(side="top", fill="both", expand="yes")

    # Display the description
    description_label = tk.Label(root, text=description, wraplength=500)
    description_label.pack(side="bottom", fill="x", expand="yes")

    root.mainloop()


if __name__ == '__main__':

    image_path = path_config.screenshot_path

    display_gui(image_path, ImDescribe())
