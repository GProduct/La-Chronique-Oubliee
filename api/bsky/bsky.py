from dotenv import load_dotenv
import os
from atproto import Client, client_utils
import logging

logger = logging.getLogger(__name__)

load_dotenv('.env')

username = os.getenv('BSKY_USERNAME')
password = os.getenv('BSKY_PASSWORD')

def connect(client):
    logger.info("Logging in to Bluesky user=%s", username)
    try:
        client.login(username, password)
    except Exception:
        logger.exception("Failed to login to Bluesky")
        raise
        
def post(client : Client, tb: client_utils.TextBuilder, image, image_alt):
    try:
        client.send_image(tb, image=image, image_alt=image_alt)
        logger.info("Post sent to Bluesky")
        return True
    except Exception as e:
        logger.exception("Failed to send image/post to Bluesky")
        return False
