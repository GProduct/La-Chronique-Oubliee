import requests
import xml.etree.ElementTree as ET
import os
import random
from title_filters_utils import load_forbidden_words
from title_filters_utils import contains_forbidden_words

elements = {
    'title': [],
    'linkDate': [],
    'link': [],
    'couverture': []
}

forbidden_words = load_forbidden_words("./filters/forbidden_words.json")

def getGallicaReferences(year, month, day):
    sru_endpoint_highRes = "https://gallica.bnf.fr/SRU"
    params = {
        'version': '1.2',
        'operation': 'searchRetrieve',
        'query': f"""dc.type any fascicule and dc.date all {year}{month}{day} and dc.language any fre or dc.language any frm or dc.language any fro""",
        'recordSchema': 'dc',
        'startRecord': 1,
        'maximumRecords': 20
    }
    response = requests.get(sru_endpoint_highRes, params=params)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        ns = {'srw': 'http://www.loc.gov/zing/srw/',
              'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
              'dc': 'http://purl.org/dc/elements/1.1/'}

        for record in root.findall('.//srw:record', ns):
            title = record.find('.//dc:title', ns)
            if title is not None:
                elements['title'].append(title.text)
            else:
                elements['title'].append(None)
            linkDate = record.find('.//dc:identifier', ns)
            if linkDate is not None:
                elements['linkDate'].append(linkDate.text)
            else:
                elements['linkDate'].append(None)
            couverture = record.find('.//highres', ns)
            if couverture is not None:
                link = couverture.text.removesuffix('.highres')
                elements['couverture'].append(couverture.text)
                elements['link'].append(link)
            else:
                elements['couverture'].append(None)
                elements['link'].append(None)
    else:
        print(f"Erreur {response.status_code} lors de la requête à l'API SRU")

    index = random.randint(0, len(elements['title']) - 1)
    title = elements['title'][index]
    link = elements['link'][index]
    highResCover = elements['couverture'][index]

    if contains_forbidden_words(title, forbidden_words):
        print("Titre contenant des mots interdits, nouvelle recherche...")
        return getGallicaReferences(year, month, day)
    else:
        return title, link, highResCover

def parseImage(highResCoverLink, docId, date):
    # On récupère l'identifiant de la couverture
    identifiant = highResCoverLink.removesuffix(".highres").removeprefix("https://gallica.bnf.fr/ark:/12148/")

    # On récupère l'image en haute résolution
    sru_endpoint_highRes = highResCoverLink

    # On récupère l'image en résolution native
    sru_endpoint_nativeRes = f"https://gallica.bnf.fr/iiif/ark:/12148/{identifiant}/f1/full/full/0/native.jpg"

    # On récupère l'image en résolution moyenne
    sru_endpoint_medRes = highResCoverLink.removesuffix(".highres") + ".medres"

    # On crée le dossier de stockage
    os.makedirs(f"result/{date}/{docId}", exist_ok=False)

    # On télécharge les images
    response_highRes = requests.get(sru_endpoint_highRes)
    if response_highRes.status_code == 200:
        with open(f"result/{date}/{docId}/highResCover.jpg", 'wb') as file:
            file.write(response_highRes.content)
    else:
        print(f"Erreur {response_highRes.status_code} lors de la requête à l'API IIIF")


    response_nativeRes = requests.get(sru_endpoint_nativeRes)
    if response_nativeRes.status_code == 200:
        with open(f"result/{date}/{docId}/nativeResCover.jpg", 'wb') as file:
            file.write(response_nativeRes.content)
    else:
        print(f"Erreur {response_nativeRes.status_code} lors de la requête à l'API IIIF")

    response_medRes = requests.get(sru_endpoint_medRes)
    if response_medRes.status_code == 200:
        with open(f"result/{date}/{docId}/medResCover.jpg", 'wb') as file:
            file.write(response_medRes.content)
    else:
        print(f"Erreur {response_medRes.status_code} lors de la requête à l'API IIIF")
    
    return sru_endpoint_nativeRes, f"result/{date}/{docId}/highResCover.jpg", f"result/{date}/{docId}/nativeResCover.jpg", f"result/{date}/{docId}/medResCover.jpg"