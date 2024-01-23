# import tkinter as tk
# from tkinter import ttk

# def create_text_widgets(root, gpt_response):
#     text_widgets = []
#     current_text = ""
#     is_code_section = False

#     for line in gpt_response.split('\n'):
#         if line.strip().startswith("```"):
#             if is_code_section:
#                 text_widget = tk.Text(root, wrap='none', font=('Consolas', 15))
#                 text_widget.insert('end', current_text)
#                 text_widget.config(state='disabled')
#                 text_widget.pack(expand=True, fill='both', padx=10, pady=10, anchor='w')
#                 text_widgets.append(text_widget)
#             else:
#                 label = tk.Label(root, text=current_text, font=('Arial', 15), fg='white', wraplength=600, justify='center', anchor='w')
#                 label.pack()
#             is_code_section = not is_code_section
#             current_text = ""
#         else:
#             current_text += line + '\n'

#     if current_text.strip() and not is_code_section:
#         label = tk.Label(root, text=current_text, font=('Arial', 15), fg='white', wraplength=600, justify='center', anchor='w')
#         label.pack()
#     elif current_text.strip():
#         text_widget = tk.Text(root, wrap='none', font=('Consolas', 14))
#         text_widget.insert('end', current_text)
#         text_widget.config(state='disabled')
#         text_widget.pack(expand=True, fill='both', padx=10, pady=10, anchor='w')
#         text_widgets.append(text_widget)

#     return text_widgets

# def main():
#     root = tk.Tk()
#     root.title("GPT Response")

#     # Load the GPT response from a file or wherever you have it
#     file_path = '/Users/panoskolyvakis/VSprojects/ImageTOtext/output.txt'
#     with open(file_path, "r") as file:
#         gpt_response = file.read()

#     # Create text widgets for code and labels for non-code sections
#     text_widgets = create_text_widgets(root, gpt_response)

#     root.mainloop()

# if __name__ == "__main__":
#     main()
import tkinter as tk
from tkinter import ttk

def create_text_widgets(root, gpt_response):
    text_widgets = []
    current_text = ""
    is_code_section = False

    for line in gpt_response.split('\n'):
        if line.strip().startswith("```"):
            if is_code_section:
                frame = tk.Frame(root)
                frame.pack(expand=True, fill='both', padx=10, pady=10)

                text_widget = tk.Text(frame, wrap='none', font=('Consolas', 15))
                text_widget.insert('end', current_text)
                text_widget.config(state='disabled')
                text_widget.pack(side='left', expand=True, fill='both', padx=5, pady=5, anchor='w')
                text_widgets.append(text_widget)
                
                # Create "Copy Code" button for the current code section
                copy_button = tk.Button(frame, text="Copy Code", command=lambda widget=text_widget: copy_code(widget))
                copy_button.pack(side='right', padx=5, pady=5)
            else:
                label = tk.Label(root, text=current_text, font=('Arial', 15), fg='white', wraplength=600, justify='center', anchor='w')
                label.pack()
            is_code_section = not is_code_section
            current_text = ""
        else:
            current_text += line + '\n'

    if current_text.strip() and not is_code_section:
        label = tk.Label(root, text=current_text, font=('Arial', 15), fg='white', wraplength=600, justify='center', anchor='w')
        label.pack()
    elif current_text.strip():
        frame = tk.Frame(root)
        frame.pack(expand=True, fill='both', padx=10, pady=10)

        text_widget = tk.Text(frame, wrap='none', font=('Consolas', 14))
        text_widget.insert('end', current_text)
        text_widget.config(state='disabled')
        text_widget.pack(side='left', expand=True, fill='both', padx=5, pady=5, anchor='w')
        text_widgets.append(text_widget)

    return text_widgets

def copy_code(widget):
    selected_text = widget.get("1.0", "end-1c")
    root.clipboard_clear()
    root.clipboard_append(selected_text)

def main():
    global root
    root = tk.Tk()
    root.title("GPT Response")

    # Load the GPT response from a file or wherever you have it
    file_path = '/Users/panoskolyvakis/VSprojects/ImageTOtext/output.txt'
    with open(file_path, "r") as file:
        gpt_response = file.read()

    # Create text widgets for code and labels for non-code sections
    text_widgets = create_text_widgets(root, gpt_response)

    root.mainloop()

if __name__ == "__main__":
    main()

