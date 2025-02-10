import xml.etree.ElementTree as ET
from utils.utils import getRandomNumber, getCurrentDate
import requests
import os

def downloadImage(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)
        file.close()
        
def isDocumentAlreadyProcessed(uri):
    if os.path.exists('./temp/processed_documents.csv'):
        with open('./temp/processed_documents.csv', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                if uri in line:
                    return True
    return False

def writeUriToLog(uri):
    with open('./temp/processed_documents.csv', 'a', encoding='utf-8') as file:
        file.write(f"{uri}, {getCurrentDate()}\n")
        file.close()

def blankLog():
    if os.path.exists('./temp/processed_documents.csv'):
        with open('./temp/processed_documents.csv', 'r+', encoding='utf-8') as file:
            lines = file.readlines()
            if lines and lines[-1].strip().endswith(getCurrentDate()):
                return
            file.seek(0)
            file.truncate()
            file.write("uri, date\n")
    else:
        with open('./temp/processed_documents.csv', 'w', encoding='utf-8') as file:
            file.write("uri, date\n")