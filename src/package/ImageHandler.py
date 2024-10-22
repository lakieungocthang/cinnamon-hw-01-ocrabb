import pytesseract
from PIL import Image
import os
import json
from langdetect import detect
import package.CustomHandler as CustomHandler



class ImageHandler(CustomHandler.CustomHandler):
    def __init__(self, type):
        super().__init__(type)

    def process(self, file):
        extracted = []
        img = Image.open(file)

        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        paragraphs = []
        current_paragraph = {"text": "", "x1": float("inf"), "y1": float("inf"), "x2": 0, "y2": 0}
        previous_bottom = 0

        for i in range(len(data['text'])):
            if int(data['conf'][i]) > 0:
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                text = data['text'][i].strip()
                if text:
                    try:
                        detected_lang = detect(text)
                    except:
                        detected_lang = 'unknown'
                    ocr_lang = 'vie' if detected_lang == 'vi' else 'eng'

                    text = pytesseract.image_to_string(img.crop((x, y, x + w, y + h)), lang=ocr_lang).strip()

                    current_top = y
                    if current_paragraph["text"] and (current_top - previous_bottom) > 20: # around 20-25 pixels
                        paragraphs.append(current_paragraph)
                        current_paragraph = {"text": "", "x1": float("inf"), "y1": float("inf"), "x2": 0, "y2": 0}

                    current_paragraph["text"] += " " + text if current_paragraph["text"] else text
                    current_paragraph["x1"] = min(current_paragraph["x1"], x)
                    current_paragraph["y1"] = min(current_paragraph["y1"], y)
                    current_paragraph["x2"] = max(current_paragraph["x2"], x + w)
                    current_paragraph["y2"] = max(current_paragraph["y2"], y + h)

                    previous_bottom = y + h

        if current_paragraph["text"]:
            paragraphs.append(current_paragraph)

        for paragraph in paragraphs:
            extracted.append({'location': (paragraph["x1"], paragraph["y1"], paragraph["x2"], paragraph["y2"]), 'page': 1, 'text': paragraph["text"]})
        return (file, extracted)
