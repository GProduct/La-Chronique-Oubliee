import requests
import os
import dotenv
import json
import logging

dotenv.load_dotenv()

COHERE_API_KEY = os.getenv('COHERE_API_KEY')
EXAMPLES_PATH = './res/examples.json'

logger = logging.getLogger(__name__)


# Chat (POST /v1/chat)
def cohereRequest(year, filename):
    logger.info("Preparing cohere request for year=%s using OCR file=%s", year, filename)
    with open(filename, 'r', encoding='utf-8') as ocr_file:
        ocr = ocr_file.read().strip()

    # load example data
    try:
        with open(EXAMPLES_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except Exception as e:
        logger.exception("Failed to load cohere examples from %s", EXAMPLES_PATH)
        raise

    url = 'https://api.cohere.com/v1/chat'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {COHERE_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'message': f'Vous \u00eates en {year}, voici la Une du jour: \"{ocr}\"',
        'chat_history': data['chat_history'],
        'max_input_tokens': data['max_input_tokens'],
        'model': data['model'],
        'preamble': data['preamble']
    }

    try:
        logger.info(f"Sending request to Cohere API at {url}")
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
        response.raise_for_status()
    except Exception as e:
        logger.exception("Cohere API request failed")
        raise

    json_response = json.loads(response.text)

    os.makedirs('./temp', exist_ok=True)
    with open('./temp/cohere_response.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(json_response, indent=4))
    logger.info("Cohere response written to ./temp/cohere_response.json")
    return json_response.get('text')