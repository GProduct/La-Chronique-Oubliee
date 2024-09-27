import pytesseract
from PIL import Image
import PIL
import os
import datetime

# Chemin vers l'exécutable Tesseract si nécessaire
#pytesseract.pytesseract.tesseract_cmd = r"./utils/tesseract/tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

def getOCR(docId):
    path = f"""result/{datetime.datetime.now().strftime('%Y-%m-%d')}/{docId}/"""
    image = PIL.Image.open(f"{path}nativeResCover.jpg")
    texte = pytesseract.image_to_string(image)
    with open(f"{path}ocr.txt", 'w', encoding='utf-8') as file:
        file.write(texte)
    return texte