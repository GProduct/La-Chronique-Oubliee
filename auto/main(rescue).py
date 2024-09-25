import requests
import xml.etree.ElementTree as ET
import datetime
import random
import os
import google.generativeai as genai
import PIL
from io import BytesIO
import requests
import json
import pytesseract
from PIL import Image
from twitter import postTweet

# Chemin vers l'exécutable Tesseract si nécessaire
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

elements = {
    'title': [],
    'linkDate': [],
    'link': [],
    'couverture': []
}

def bissex(year):
    if year%4==0 and not year%100==0:
        return True
    else:
        return False

def chooseRandomDate():
    day = datetime.datetime.now().day
    day = str(day).zfill(2)
    month = datetime.datetime.now().month
    month = str(month).zfill(2)
    year = random.randint(1880, 1955)
    if month == 2 and day > 28:
        while not bissex(year):
            year = random.randint(1880, 1955)
    else:
        pass
    return year, month, day

def getGallicaReferences(year, month, day):
    sru_endpoint = "https://gallica.bnf.fr/SRU"
    params = {
        'version': '1.2',
        'operation': 'searchRetrieve',
        'query': f"""dc.type any fascicule and dc.date all {year}{month}{day} and dc.language any fre or dc.language any frm or dc.language any fro""",
        'recordSchema': 'dc',
        'startRecord': 1,
        'maximumRecords': 20
    }
    # Faire une requête à l'API SRU de la BnF
    response = requests.get(sru_endpoint, params=params)

    if response.status_code == 200:
        # Parsez la réponse XML
        root = ET.fromstring(response.content)
        # Traitez les enregistrements
        ns = {'srw': 'http://www.loc.gov/zing/srw/',
            'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
            'dc': 'http://purl.org/dc/elements/1.1/'}

        for record in root.findall('.//srw:record', ns) :
            title = record.find('.//dc:title', ns)
            if title is not None:
                print(f"Titre : {title.text}")
                elements['title'].append(title.text)
            else:
                elements['title'].append(None)
                print(f"Titre : None")
            linkDate = record.find('.//dc:identifier', ns)
            if linkDate is not None:
                elements['linkDate'].append(linkDate.text)
                print(f"Lien vers les numéros : {linkDate.text}")
            else:
                elements['linkDate'].append(None)
                print(f"Couverture : None")
            couverture = record.find('.//highres', ns)
            if couverture is not None:
                link = couverture.text.removesuffix('.highres')
                elements['couverture'].append(couverture.text)
                elements['link'].append(link)
                print(f"Couverture : {couverture.text}")
                print(f"Lien : {link}\n")
            else:
                elements['couverture'].append(None)
                elements['link'].append(None)
                print(f"Couverture : None")
                print(f"Lien : None\n")
        print("\nPremière requête SRU terminée avec succès\n")
    else:
        print(f"Erreur {response.status_code} lors de la requête à l'API SRU")

    #Parmis la liste des éléments, on veut en prendre un au hasard
    index = random.randint(0, len(elements['title'])-1)
    titleFinal = elements['title'][index]
    linkFinal = elements['link'][index]
    couvertureFinal = elements['couverture'][index]

    return titleFinal, linkFinal, couvertureFinal

def parseImage(couvertureFinal, docId):
    print("\n")
    identifiant = couvertureFinal.removesuffix(".highres").removeprefix("https://gallica.bnf.fr/ark:/12148/")
    page = 1
    sru_endpoint_bis = f"https://gallica.bnf.fr/iiif/ark:/12148/{identifiant}/f1/full/full/0/native.jpg"
    print(f"lien de l'image haute qualité {sru_endpoint_bis}")
    print(f"enregirstrement à .result/{docId}/cover.jpg")
    os.makedirs(f"result/{docId}", exist_ok=True)

    response = requests.get(sru_endpoint_bis)
    if response.status_code == 200:
        with open(f"result/{docId}/cover.jpg", 'wb') as file:
            file.write(response.content)
        print("Image téléchargée avec succès.")
    else:
        print(f"Erreur {response.status_code} lors de la requête à l'API IIIF")
    
    return sru_endpoint_bis

def getOCR(sru_endpoint_bis, docId):
    print("\n")
    print(f"Exécution de l'OCR sur l'image")
    path = f"result/{docId}/cover.jpg"
    
    image = PIL.Image.open(path)

    # Utilise pytesseract pour faire de l'OCR sur l'image
    texte = pytesseract.image_to_string(image)
    # Écrire le contenu de l'OCR dans un fichier texte
    with open(f"""result/{docId}/ocr.txt""", 'w', encoding='utf-8') as file:
        file.write(texte)
    print("Fichier ocr.txt créé avec succès.")
    print(f"Texte de l'image :\n {texte}")
    return texte

def getTinyURL(longUrl):
    tinyUrl = "http://tinyurl.com/api-create.php?url="
    tinyUrlResponse = requests.get(tinyUrl+longUrl)
    short_url = tinyUrlResponse.text
    return short_url

def getRecap(title, link, coverLink, texte, tinyLink):
    print("\n")
    print(f"Titre du fascicule : {title}")
    print(f"Lien vers les numéros : {link}")
    print(f"Lien de l'image : {coverLink}")
    print(f"Le lien raccourci : {tinyLink}")
    #print(f"Texte extrait de l'image : {texte}")

def main():
    year, month, day = chooseRandomDate()
    title, link, cover = getGallicaReferences(year, month, day)
    docId = link.removeprefix("https://gallica.bnf.fr/ark:/12148/")
    tinyLink = getTinyURL(link)
    coverLink = parseImage(cover, docId)
    texte = getOCR(coverLink, docId)
    getRecap(title, link, coverLink, texte, tinyLink)

main()