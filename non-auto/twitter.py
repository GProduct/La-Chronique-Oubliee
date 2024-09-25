import json
import os
import time
import traceback
import tweepy

# Your Twitter API credentials
consumer_key = os.getenv('X_CONSUMER_KEY')
consumer_secret = os.getenv('X_CONSUMER_SECRET')
access_token = os.getenv('X_ACCESS_TOKEN')
access_token_secret = os.getenv('X_ACCESS_TOKEN_SECRET')

def postTweet(content, mediaPath = None):
    # Create API object
    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )

    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret
    )

    api = tweepy.API(auth)

    if mediaPath is not None:
        # test if media exists and if its an image
        if os.path.isfile(mediaPath) and mediaPath.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            media = api.media_upload(mediaPath)
            api.update_status(status=content, media_ids=[media.media_id])
    else:
        client.create_tweet(text=content)