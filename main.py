from api.bnf.gallica import mainGallica
from api.cohere.cohere import cohereRequest
from atproto import Client, client_utils
from api.bsky.bsky import connect, post
from api.bsky.bsky_utils import formatPost
  
result = mainGallica()

print(f"Result: {result['data']['search_year']} - {result['data']['uri']}")

while True:
    post_content = cohereRequest(year=result['data']['search_year'], filename=f'./temp/{result["data"]["uri"]}-ocr.txt')
    print(f"Post: {post_content}")
    client = Client()
    tb, image, image_alt = formatPost(result, post_content)
    length = len(tb.build_text())
    if length <= 300 :
        print(f"Post content length: {length}, sending post...")
        break
    else:
        print(f"Post content length: {length}, trying again...")

connect(client)
if post(client, tb, image, image_alt):
    print("Post sent successfully !")
else:
    print("Error while sending post.")