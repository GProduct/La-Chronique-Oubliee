import json

def load_forbidden_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['forbidden_words']

def contains_forbidden_words(title, forbidden_words):
    for word in forbidden_words:
        if word.lower() in title.lower():
            return True
    return False