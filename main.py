from api.bnf.gallica import mainGallica
from api.cohere.cohere import cohereRequest
from atproto import Client, client_utils
from api.bsky.bsky import connect, post
from api.bsky.bsky_utils import formatPost

result = mainGallica()

print(f"Result: {result['data']['search_year']} - {result['data']['uri']}")

post_content = cohereRequest(year=result['data']['search_year'], filename=f'./temp/{result["data"]["uri"]}-ocr.txt')

print(post_content)

client = Client()
connect(client)

tb, image, image_alt = formatPost(result, post_content)

post(client, tb, image, image_alt)