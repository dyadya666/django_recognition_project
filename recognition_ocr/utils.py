import os
import pytesseract

from PIL import Image


def extract_text(file_path):
    """
    Витягує текст із зображення (PNG, JPG) або PDF.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".png", ".jpg", ".jpeg"]:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img, lang="ukr+eng")
    elif ext == ".pdf":
        # для PDF використовуємо pdf2image
        from pdf2image import convert_from_path
        pages = convert_from_path(file_path)
        text = "\n".join(pytesseract.image_to_string(p, lang="ukr+eng") for p in pages)
    else:
        text = ""
        
    return text
