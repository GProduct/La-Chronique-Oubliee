import pytesseract
import PIL
import dotenv
import os
import logging

dotenv.load_dotenv()

pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_OCR_PATH")
logger = logging.getLogger(__name__)


def executeOCR(filename, path, lang='fra'):
    logger.info("Executing OCR on %s -> %s", path, filename)
    try:
        image = PIL.Image.open(path)
        text = pytesseract.image_to_string(image, lang=lang)
    except Exception:
        logger.exception("OCR failed for %s", path)
        raise
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)
    logger.info("OCR written to %s (chars=%s)", filename, len(text))