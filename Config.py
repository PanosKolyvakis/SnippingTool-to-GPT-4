import os

class PathConfig:
    def __init__(self):
        self.ocr_output_path = os.getenv('OCR_OUTPUT_PATH', '/default/path/for/OCRextracted_text.txt')
        self.api_output_path = os.getenv('API_OUTPUT_PATH', '/default/path/for/output.txt')
        self.screenshot_path = os.getenv('SCREENSHOT_PATH', '/default/path/for/screenshot.png')
        self.api_key = os.getenv('OPENAI_API_KEY', 'default_api_key')
        self.image_graphic = os.getenv('IMAGE_GRAPHIC_PATH', '/default/path/for/ImageGraphic.png')
