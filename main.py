import tweepy
import requests
import json
import os
import datetime
from os import environ


consumer_key = environ['CONSUMER_KEY']
consumer_secret = environ['CONSUMER_SECRET']
access_token = environ['ACCESS_TOKEN']
access_token_secret = environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

posted = False

while True:

    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute

    if hour == 10 and minute == 0 and posted == False:
        api = tweepy.API(auth)
        nasa_api = environ['NASA_API']
        response = requests.get(nasa_api)
        data = response.json()
        media_url = data["url"]

        response = requests.get(media_url)
        title = data["title"]

        woeid = 2282863

        trends = api.trends_place(id = woeid)
        tags = ""
        count = 0

        for value in trends:
            for trend in value['trends']:
                if trend['name'][0] == '#':
                    tags += trend['name'] + " "
                    count += 1
                if count > 7:
                    break
            if count > 7:
                break

        tweet = title + '.\n' + '\n' + tags

        image_path = "image.png"
        video_path = "video.mp4"

        if data["media_type"] != "video":
            with open(image_path, 'wb') as img:
                img.write(response.content)
            status = api.update_with_media(image_path, tweet)
            posted = True
        
        

    if hour == 10 and minute == 5:
        posted = False
