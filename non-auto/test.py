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
    'couverture': [],
    'date': []
}

forbidden_words = load_forbidden_words("./filters/forbidden_words.json")

def searchOnGallica(subject):
    #on va faire une requête sur l'API SRU de Gallica
    sru_endpoint_search = "https://gallica.bnf.fr/SRU"
    params = {
        'version': '1.2',
        'operation': 'searchRetrieve',
        'query': f"""gallica all "{subject}" and dc.type any fascicule and dc.language any fre or dc.language any frm or dc.language any fro""",
        'recordSchema': 'dc',
        'startRecord': 1,
        'maximumRecords': 20
    }
    response = requests.get(sru_endpoint_search, params=params)
    print(response.url)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        ns = {'srw': 'http://www.loc.gov/zing/srw/',
              'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
              'dc': 'http://purl.org/dc/elements/1.1/'}

        for record in root.findall('.//srw:record', ns):
            title = record.find('.//dc:title', ns)
            if title is not None:
                elements['title'].append(title.text)
                print(title.text)
            else:
                elements['title'].append(None)

            linkDate = record.find('.//dc:identifier', ns)
            if linkDate is not None:
                elements['linkDate'].append(linkDate.text)
                print(linkDate.text)
            else:
                elements['linkDate'].append(None)

            link = record.find('.//link', ns)
            if link is not None:
                elements['link'].append(link.text)
                print(link.text)
            else:
                elements['link'].append(None)

            couverture = record.find('.//highres', ns)
            if couverture is not None:
                elements['couverture'].append(couverture.text)
            else:
                elements['couverture'].append(None)
                elements['link'].append(None)
            
            date = record.find('.//dc:date', ns)
            if date is not None:
                elements['date'].append(date.text)
                print(date.text)
            else:
                elements['date'].append(None)
    else:
        print(f"Erreur {response.status_code} lors de la requête à l'API SRU")

searchOnGallica("Zeramdine")            