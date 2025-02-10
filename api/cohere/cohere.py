import requests
import os
import dotenv
import json

dotenv.load_dotenv()

COHERE_API_KEY = os.getenv('COHERE_API_KEY')
EXAMPLES_PATH = './res/examples.json'

# Chat (POST /v1/chat)
def cohereRequest(year, filename):
    with open(filename, 'r', encoding='utf-8') as ocr_file:
        ocr = ocr_file.read().strip()
        ocr_file.close()
    
    # load example data
    with open(EXAMPLES_PATH, 'r', encoding='utf-8') as file:
        data = json.load(file)
        file.close()
        
    url = 'https://api.cohere.com/v1/chat'
    headers = {
		'accept': 'application/json',
		'Authorization': f'Bearer {COHERE_API_KEY}',
		'Content-Type': 'application/json'
	}
    data = {
		'message': f'Vous êtes en {year}, voici la Une du jour: \"{ocr}\"',
		'chat_history': data['chat_history'],
		'max_input_tokens': data['max_input_tokens'],
		'model': data['model'],
		'preamble': data['preamble']
	}
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    json_response = json.loads(response.text)
    
    with open('./temp/cohere_response.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(json_response, indent=4))
        file.close()
    
    return json_response['text']