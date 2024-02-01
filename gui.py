
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from Config import PathConfig

PathConfig = PathConfig()
def run_gui():
    def get_selected_prompt():
        selected_value = prompt_var.get()
        if selected_value in prompts_instructions.keys():
            return selected_value
        else:
            return ''

    def get_custom_prompt():
        return custom_prompt_text.get("1.0", tk.END).strip()
        
    def get_selected_model():
        return gpt_var.get() 


    def update_textbox(final_prompt):

        for widget in output_frame.winfo_children():
            widget.destroy()

        output_text = tk.Text(output_frame, height=50, width=140)

        # Define custom tags
        output_text.tag_configure('final_prompt_style', foreground='green', font=('Arial', 13, 'bold'))
        output_text.tag_configure('ocr_text_style', foreground='red', font=('Arial', 13, 'bold'))
        output_text.tag_configure('general_text' , foreground= 'white' , font = ('Arial' , 13 ))
        # Insert text with tags
        output_text.insert(tk.END, "Final Query to GPT: \n", 'final_prompt_style')
        output_text.insert(tk.END, f"{final_prompt}\n\n " , 'general_text')

        with open(PathConfig.ocr_output_path, 'r') as file:
            extracted_text = file.read()

        output_text.insert(tk.END, "Text extracted using OCR model (Feel Free to Edit !): \n\n", 'ocr_text_style')
        output_text.insert(tk.END, extracted_text, 'general_text')

        output_text.pack()

        

    def submit_and_close():
        try:
            global selected_prompt, selected_model, custom_prompt , final_prompt
            selected_prompt = get_selected_prompt()
            selected_model = get_selected_model()
            custom_prompt = get_custom_prompt()
            # building the final prompt (dropbox , textbox or combined)
            if selected_prompt and not custom_prompt:
                final_prompt = prompts_instructions.get(selected_prompt, '')
                if custom_prompt != '':
                    final_prompt = custom_prompt
            else:
                
                final_prompt = prompts_instructions.get(selected_prompt, '') + ' ' + custom_prompt

            update_textbox(final_prompt)

        except Exception as e:
            update_textbox(e)
    root = tk.Tk()
    root.geometry("500x600+0+0")
    style = ttk.Style(root)
    style.theme_use('clam') 
    root.title("OpenAI - GPT Response")
    root.configure(bg = '#FAF0E6')
    gpt_var = tk.StringVar(root)
    output_frame = tk.Frame(root)
    output_frame.pack(fill='both', expand=True)
    gpt_models = {'GPT-4' : 'GPT-4' , 'GPT-4-Turbo' : 'gpt-4-1106-preview' ,  'GPT-3.5' : 'gpt-3.5-turbo-1106' , 'gtp-4-vision' :'gpt-4-vision-preview'}

    prompt_menu = ttk.Combobox(root, textvariable=gpt_var ,values=list(gpt_models.keys()) )

    gpt_var.set('GPT-4-Turbo' )

    prompt_menu.pack(pady=5, padx=8)
    image = Image.open(PathConfig.image_graphic) 

    # Resize the image to desired size, e.g., (width, height)
    image = image.resize((380, 350))
    photo = ImageTk.PhotoImage(image)

    # Create a label to display the image
    image_label = tk.Label(root, image=photo , bg = '#FAF0E6' , fg = 'black')
    image_label.image = photo 
    image_label.pack()
    prompt_var = tk.StringVar(root)
    question_label = tk.Label(root, text="What do you want to know? - Select from the dropdown box " , bg = '#FAF0E6' , fg= 'black')

    question_label.pack(pady=5, padx=5)
    
    prompts_instructions = {
        'Verbal reasoning test': "Verbal reasoning test: if this contains many letters or possible answers please answer only from the text and return the best answer deduced only from the text",
        'General overview': "Give me a general overview of this text, what does the author mean",
        'Coding question': "this is a coding question, please return your best effort in writing code to solve the question",
        'Rewrite this Text': 'Rewrite the following text',
        'Explain code': 'write this code line by line in different boxes and explain each line of the code separately. Use ``` important: dont specify the coding language (e.g python) here you return just the line of code ```.'
        # these ``` are used on how the IDE.py works. please do not edit
    }

    prompt_menu = ttk.Combobox(root, textvariable=prompt_var, values=list(prompts_instructions.keys()))
    prompt_menu.pack(pady=5, padx=5)

    custom_prompt_label = tk.Label(root, text = "  Enter your custom prompt below, or supplement selected prompt  " , bg = '#FAF0E6' , fg = 'black')
    custom_prompt_label.pack()
    custom_prompt_text = tk.Text(root, height=5, width=40, bg='#F0F0F0', fg='black')
    custom_prompt_text.pack(pady=10, padx=5)

    submit_button = ttk.Button(root, text="Submit", command=submit_and_close, style="TButton")
    submit_button.pack(pady=5, padx=5)

    # configure the submit button 
    style.configure("TButton", background="#F5F5F5", foreground="black", font=('Helvetica', 14))
    submit_button.pack(pady=5, padx=5)

    def close_window():
        root.destroy()

    close_button = ttk.Button(root, text="Close", command=close_window, style="TButton")
    close_button.pack(pady=5, padx=5)


    root.mainloop()


    # building the final prompt (dropbox , textbox or combined)
    if selected_prompt and not custom_prompt:
        final_prompt = prompts_instructions.get(selected_prompt, '')
        if custom_prompt != '':
            final_prompt = custom_prompt
    else:
        
        final_prompt = prompts_instructions.get(selected_prompt, '') + ' ' + custom_prompt


    return final_prompt if final_prompt else None, gpt_models[selected_model]

if __name__ == '__main__':

    run_gui()
