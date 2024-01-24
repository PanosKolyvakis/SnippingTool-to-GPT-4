import tkinter as tk
from tkinter import ttk
import re

class config:
    font_size = 15
    font_type = 'Helvetica'
    code_font_type = 'Consolas'
    file_path = 'your_file_path'
    multiple_test_path = '/any_Test'
    # window size 
    window_width = 800  # Width in pixels
    window_height = 600  # Height in pixels


def apply_code_highlighting(text_widget):
    # Dictionary mapping syntax groups to colors
    syntax_colors = {
        'class' : '#98FB98' ,
        'keyword': '#1976D2',
        'builtin': '#D32F2F',
        'string': 'green',
        'boolean': 'purple',
        
        'decorator': 'magenta',

    }
    syntax_patterns = {
        'class': ['class' , 'self'],
        'keyword': ['def', 'if', 'else', 'elif', 'while', 'for', 'break', 'continue', 'try', 'except', 'with', 'as', 'yield', 'range' , 'return'],
        'builtin': ['print', 'len', 'open', 'int', 'str', 'float', 'type', 'format', 'min', 'max', 'sum', 'list', 'dict', 'set', 'tuple'],
        'string': r'\"[^\"]*\"|\'[^\']*\'',  
        'boolean': ['True', 'False', 'None'],
        'decorator': ['@']

}

    # Configure tags in the text widget for each syntax group
    for syntax_group, color in syntax_colors.items():
        text_widget.tag_configure(syntax_group, foreground=color)

    # Apply syntax highlighting for each syntax group
    for syntax_group, patterns in syntax_patterns.items():
        if syntax_group == 'string' or syntax_group == 'operator':
            # Handle regular expressions (like string literals and operators)
            start_idx = '1.0'
            while True:
                start_idx = text_widget.search(patterns, start_idx, stopindex='end', regexp=True)
                if not start_idx:
                    break
                end_idx = f"{start_idx} lineend"
                text_widget.tag_add(syntax_group, start_idx, end_idx)
                start_idx = end_idx
        else:
            # Handle normal word lists
            for word in patterns:
                start_idx = '1.0'
                while True:
                    start_idx = text_widget.search(r'\m{}\M'.format(word), start_idx, stopindex='end', regexp=True)
                    if not start_idx:
                        break
                    end_idx = f"{start_idx}+{len(word)}c"
                    text_widget.tag_add(syntax_group, start_idx, end_idx)
                    start_idx = end_idx


def create_label_widget(root, text):
    """Create a label for non-code text."""

    def on_label_resize(event):
        label.config(wraplength=event.width)

    root.geometry(f"{config.window_width}x{config.window_height}")

    label = tk.Label(root, text=text, font=(config.font_type, config.font_size))
    label.pack(fill='both', expand=True, padx=5, pady=5)
    label.bind('<Configure>', on_label_resize)

    return label



def create_code_text_widget(frame, code_text):
    """Create a Text widget for a block of code."""
    max_height = 3

    text_widget = tk.Text(frame, wrap='none', font=(config.code_font_type, config.font_size), height=max_height)

    apply_code_highlighting(text_widget)

    lines = code_text.split('\n')
    for line in lines:
        # Calculate the current line's indentation (number of leading spaces)
        indentation = len(line) - len(line.lstrip())
        
        # Insert the line with the correct indentation
        text_widget.insert('end', ' ' * indentation + line.lstrip() + '\n')

    if len(lines) > max_height:
        # If there are more lines than the maximum height, add a vertical scrollbar
        scroll_y = tk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side='right', fill='y')

    text_widget.pack(side='left', expand=True, fill='both', padx=3, pady=3)
    text_widget.config(state='disabled')

    copy_button = tk.Button(frame, text="Copy", command=lambda widget=text_widget: copy_code(widget))
    copy_button.pack(side='bottom', padx=5, pady=5)
    
    return apply_code_highlighting(text_widget)



def copy_code(widget):
    selected_text = widget.get("1.0", "end-1c")
    root.clipboard_clear()
    root.clipboard_append(selected_text)


def find_code(response):
    sections = []
    is_code = False
    delimiter = "```"
    i = 0
    start_index = 0  

    while i < len(response):
        if response[i:i + len(delimiter)] == delimiter:
            # Add the current section (code or non-code)
            section_text = response[start_index:i].strip()
            if len(section_text) > 3:  # Check length of the text
                sections.append([section_text, is_code])

            is_code = not is_code 
            i += len(delimiter)
            start_index = i  
        else:
            i += 1

    # Add the final section if there's any remaining text
    final_section_text = response[start_index:].strip()
    if len(final_section_text) > 5:
        sections.append([final_section_text, is_code])

    def clean_noncode_text(text):
        # Pattern to match: \n\n followed by a number and a dot
        pattern = r'\n+\s*\d+\.'  
        match = re.search(pattern, text)
        if match:
            return text[:match.start()].strip()  # Return text up to the matched pattern
        return text  # Return original text if no pattern is found

    for i in range(len(sections)):
        if not sections[i][1]:

            sections[i][0] = clean_noncode_text(sections[i][0]) 

    return sections



def calculate_window_size(gpt_response, max_width=config.window_width, max_height=config.window_height, char_width=8, line_height=20):
    lines = gpt_response.split('\n')
    num_lines = len(lines)
    max_line_length = max(len(line) for line in lines)

    width = min(max_line_length * char_width, max_width)
    height = min(num_lines * line_height, max_height)

    return width, height



def main_s():
    global root
    root = tk.Tk()
    root.title("GPT Response")

    file_path = config.file_path
    with open(file_path, "r") as file:
        gpt_response = file.read()

    parsed_sections = find_code(gpt_response)
    for section_text, is_code_section in parsed_sections:
        if is_code_section:
            frame = tk.Frame(root)
            frame.pack(expand=True, fill='both', padx=3, pady=3)
            create_code_text_widget(frame, section_text)
        else:
            create_label_widget(root, section_text)

    root.mainloop()

if __name__ == '__main__':
    main_s()

