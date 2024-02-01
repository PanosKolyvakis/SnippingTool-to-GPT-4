import tkinter as tk
from tkinter import ttk
import re
from Config import PathConfig

class config:
    font_size = 15
    font_type = 'Helvetica'
    code_font_type = 'Consolas'
    multiple_test_path = '/Users/panoskolyvakis/VSprojects/ImageTOtext/testmultiplelines.txt'
    # window size 
    window_width = 800  
    window_height = 800 
    background_color = '#FAF0E6' # shade of white in HTML syntax
    code_widget_color = '#333333'



def apply_code_highlighting(text_widget , delimiter ="```" ):
    # Dictionary mapping syntax groups to colors
    syntax_colors = {
        'class' : '#98FB98',
        'keyword': '#1976D2',
        'builtin': '#D32F2F',
        'string': '#90EE90',
        'boolean': 'purple',
        'decorator': 'magenta',
        'comment': 'green'

    }

    syntax_patterns = {
        'class': ['class' , 'self'],
        'keyword': ['def', 'if', 'else', 'elif', 'while', 'for', 'break', 'continue', 'try', 'except', 'with', 'as', 'yield', 'range', 'return'],
        'builtin': ['print', 'len', 'open', 'int', 'str', 'float', 'type', 'format', 'min', 'max', 'sum', 'list', 'dict', 'set', 'tuple'],
        'string': r'\"[^\"]*\"|\'[^\']*\'',
        'boolean': ['True', 'False', 'None'],
        'decorator': ['@'],
        'comment': r'#.*'  # Regular expression for comments
    }

    # Configure tags in the text widget for each syntax group
    for syntax_group, color in syntax_colors.items():
        text_widget.tag_configure(syntax_group, foreground=color)

    # Apply syntax highlighting for each syntax group
    for syntax_group, patterns in syntax_patterns.items():
        if syntax_group in ['string', 'comment']:
            # Handle regular expressions (like string literals and comments)
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




# def create_label_widget(frame, text):
#     """Create a text widget for non-code text with dynamic height based on the text length and window width."""

#     def calculate_text_height(text, window_width, font_size):
#         """Estimate the number of lines the text will occupy."""
#         avg_char_width = font_size * 0.6  
#         max_chars_per_line = window_width / avg_char_width
#         lines = text.split('\n')
#         total_lines = sum(len(line) / max_chars_per_line for line in lines)
#         return max(int(total_lines), 1)  # Ensure minimum height is 1

#     text_height = calculate_text_height(text, config.window_width, config.font_size)

#     # Create a text widget with calculated height
#     text_widget = tk.Text(frame, font=(config.font_type, config.font_size), wrap='word', height=text_height, bd=0, highlightthickness=0, bg='#FAF0E6', fg='black')

#     # Insert the provided text
#     text_widget.insert('1.0', text)

#     # Make the text widget read-only
#     text_widget.config(state='disabled')

#     # Pack the text widget
#     text_widget.pack(fill='both', expand=True, padx=15, pady=15)

#     return text_widget
def create_label_widget(frame, text):
    """Create a text widget for non-code text with dynamic height based on the text length and window width."""
    def calculate_text_height(text , chars_per_line):

        """Estimate the number of lines the text will occupy based on a fixed number of characters per line."""
        total_chars = len(text)
        total_lines = total_chars / chars_per_line
        return max(int(total_lines), 1)  # Ensure minimum height is 1

    # Define the number of characters that fit into a single line
    chars_per_line = 120

    text_height = calculate_text_height(text, chars_per_line)

    # Create a text widget with calculated height
    text_widget = tk.Text(frame, font=(config.font_type, config.font_size), wrap='word',
                          height=text_height, bd=0, highlightthickness=0, bg='#FAF0E6', fg='black')

    # Insert the provided text
    text_widget.insert('1.0', text)

    # Make the text widget read-only
    text_widget.config(state='disabled')

    # Pack the text widget
    text_widget.pack(fill='both', expand=True, padx=15, pady=15)

    return text_widget



def create_code_text_widget(frame, code_text):
    """Create a Text widget for a block of code with dynamic height."""
    lines = code_text.split('\n')  # Splitting the text into lines

    max_height = len(lines)  # Calculate height based on the number of lines

    code_bg_color = '#2b2b2b'  # Background color for the code widget

    frame.config(bg=code_bg_color, bd=0, highlightthickness=0)

    text_widget = tk.Text(frame, wrap='none', font=(config.code_font_type, config.font_size),
                          height=max_height, bg=code_bg_color, fg='white',
                          bd=0, highlightthickness=0, padx=10, pady=0)

    apply_code_highlighting(text_widget)

    for line in lines:
        if line.startswith('python') or line.startswith('cpp'):
            continue
        text_widget.insert('end', line + '\n')  # Insert each line into the widget

    # Add a scrollbar if there are more lines than the height of the widget
    if max_height > 1:
        scroll_y = tk.Scrollbar(frame, orient="vertical", command=text_widget.yview, bg=code_bg_color)
        text_widget.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side='right', fill='y')

    text_widget.pack(side='top', fill='both', expand=True, padx=10, pady=2)
    text_widget.config(state='disabled')  # Making the widget read-only

    # Button for copying code
    copy_button = tk.Button(frame, text="Copy", command=lambda: copy_code(text_widget),
                            bg=code_bg_color, fg='black', relief='flat', highlightthickness=0)
    copy_button.pack(side='right', padx=10, pady=2)

    return apply_code_highlighting(text_widget , delimiter= "```")




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

    return width if width > 300 else 300 , height if height > 300 else 300




def main_s():
    global root

    path_config = PathConfig()
    # path_config.api_output_path --- > this should be run normally
    #config.multiple_test_path
    with open(path_config.api_output_path, "r") as file:
        gpt_response = file.read()
    window_width , window_height = calculate_window_size(gpt_response)
    # configuring the position, color and size of the background

    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use('clam') 
    root.title("GPT Response")

    root.geometry(f"{window_width}x{window_height}+500+0")

    root.configure(bg = '#FAF0E6')

    


    parsed_sections = find_code(gpt_response)
    for section_text, is_code_section in parsed_sections:
        if is_code_section:
            frame = tk.Frame(root)
            frame.pack(expand=True, fill='both', padx=3, pady=1)
            create_code_text_widget(frame, section_text)
        else:
            create_label_widget(root, section_text)

    root.mainloop()

# def update_scroll_region():
#     root.update_idletasks()  # Update the layout to get the correct size
#     canvas.config(scrollregion=canvas.bbox("all"))


if __name__ == '__main__':

    main_s()
