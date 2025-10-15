from api.bnf.gallica import mainGallica
from api.cohere.cohere import cohereRequest
from atproto import Client
from api.bsky.bsky import connect, post
from api.bsky.bsky_utils import formatPost
from utils.logger import setup_logging
import logging
  
# initialize logging (writes to ./logs/app.log by default)
logger = setup_logging()

logger.info("Starting La Chronique Oubliée bot...")

logger.info("Fetching data from Gallica...")
result = mainGallica()

logger.info("Result: %s - %s", result['data']['search_year'], result['data']['uri'])

while True:
    post_content = cohereRequest(year=result['data']['search_year'], filename=f"./temp/{result['data']['uri']}-ocr.txt")
    logger.debug("Post content: %s", post_content)
    client = Client()
    try:
        tb, image, image_alt = formatPost(result, post_content)
        length = len(tb.build_text())
    except Exception as e:
        logger.exception("Error processing image")
        continue
    if length <= 300 :
        logger.info("Post content length: %s, sending post...", length)
        break
    else:
        logger.info("Post content length: %s, trying again...", length)

connect(client)
if post(client, tb, image, image_alt):
    logger.info("Post sent successfully !")
else:
    logger.error("Error while sending post.")
