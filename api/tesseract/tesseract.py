import pytesseract
import PIL
import dotenv
import os

dotenv.load_dotenv()

pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_OCR_PATH")

def executeOCR(filename, path, lang='fra'):
    image = PIL.Image.open(path)
    text = pytesseract.image_to_string(image)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)