from dotenv import load_dotenv
import os
from atproto import Client, client_utils

load_dotenv('.env')

username = os.getenv('BSKY_USERNAME')
password = os.getenv('BSKY_PASSWORD')

def connect(client):
    client.login(username, password)
        
def post(client : Client, tb: client_utils.TextBuilder, image, image_alt):
    client.send_image(tb, image=image, image_alt=image_alt)
