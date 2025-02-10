import requests
from PIL import Image
from io import BytesIO
from atproto import Client, client_utils

def formatPost(document, post):
    tb = client_utils.TextBuilder()
    tb.text(f"{document['data']['search_year']} - {post}\n\n🔗 Sources: ")
    tb.mention('BnF', 'did:plc:mz574rsfbbgicfvahpp4f5r2')
    tb.text(' | ')
    tb.mention('Gallica', 'did:plc:neqmczfcvfq65kjyyie45wds')
    tb.text(' | ')
    tb.link('Article', document['data']['link'])
    tb.text('.')
    
    image = imageParser(document['data']['medres'])
    image_alt = f" Image de l’article « {document['data']['title']} », paru en {document['data']['search_year']} et issu des archives de la Bibliothèque nationale de France."
    
    return tb, image, image_alt

def imageParser(image_url):
    if image_url:
        response = requests.get(image_url)
        if response.status_code == 200:
            try:
                image = Image.open(BytesIO(response.content))
                
                img_byte_arr = BytesIO()
                image_format = image.format if image.format else "JPEG"  # Sécurisation du format
                image.save(img_byte_arr, format=image_format)
                
                return img_byte_arr.getvalue()
            except Exception as e:
                print(f"Error opening image: {e}")
        else:
            print(f"Failed to fetch image. Status code: {response.status_code}")
    return None