import requests
import xml.etree.ElementTree as ET
import random
from title_filters_utils import load_forbidden_words
from title_filters_utils import contains_forbidden_words
import datetime


def bissex(year):
    if year % 4 == 0 and not year % 100 == 0:
        return True
    else:
        return False

elements = {
    'title': [],
    'linkDate': [],
    'link': [],
    'couverture': []
}

def chooseRandomDate():
    day = datetime.datetime.now().day
    day = str(day).zfill(2)
    month = datetime.datetime.now().month
    month = str(month).zfill(2)
    year = random.randint(1880, 1955)
    if month == 2 and day > 28:
        while not bissex(year):
            year = random.randint(1870, 1955)
    else:
        pass
    return year, month, day

year, month, day = chooseRandomDate()

forbidden_words = load_forbidden_words("./filters/forbidden_words.json")

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