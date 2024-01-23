import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def run_gui():
    def get_selected_prompt():
        return prompt_var.get() or custom_prompt_text.get("1.0", tk.END).strip()

    def submit_and_close():
        global selected_prompt
        selected_prompt = get_selected_prompt()
        root.destroy()

    root = tk.Tk()
    root.title("GPT-4 Response")

    image_path = '/Users/panoskolyvakis/VSprojects/ImageToText/ImageGraphic.png'
    image = Image.open(image_path)

    # Resize the image to desired size, e.g., (width, height)
    image = image.resize((250, 230))
    photo = ImageTk.PhotoImage(image)

    # Create a label to display the image
    image_label = tk.Label(root, image=photo)
    image_label.image = photo 
    image_label.pack()
    prompt_var = tk.StringVar(root)
    question_label = tk.Label(root, text="What do you want to know?")
    question_label.pack()
    prompts = ['Verbal reasoning test', "General overview", "Coding question" , 'Rewrite this Text']
    feed_to_gpt = ["Verbal reasoning test: if this contains many letters or possible answers please answer only from the text and return the best answer deduced only from the text" , "Give me a general overview of this text, what does the author mean" , "this is a coding question, please return your best effort in writing code to solve the question" , 'Rewrite the following text']

    prompt_menu = ttk.Combobox(root, textvariable=prompt_var, values=prompts)
    prompt_menu.pack()

    custom_prompt_label = tk.Label(root, text="Or enter your custom prompt below:")
    custom_prompt_label.pack()
    custom_prompt_text = tk.Text(root, height=5, width=30)
    custom_prompt_text.pack()

    submit_button = tk.Button(root, text="Submit", command=submit_and_close)
    submit_button.pack()

    root.mainloop()

    return feed_to_gpt[prompts.index(selected_prompt)]
