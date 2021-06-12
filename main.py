import requests
import json
import os
import tweepy
from os import environ
import ntplib
import time
from time import ctime

consumer_key = environ['CONSUMER_KEY']
consumer_secret = environ['CONSUMER_SECRET']
access_token = environ['ACCESS_TOKEN']
access_token_secret = environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

posted = False

while True:

    time.sleep(10)

    ntp_client = ntplib.NTPClient()
    response = ntp_client.request('in.pool.ntp.org')
    times = ctime(response.tx_time)
    hour = int(times[11:13])
    minute = int(times[14:16])

    if hour == 16 and minute == 8 and posted == False:
        api = tweepy.API(auth)
        nasa_api = environ['NASA_API']
        response = requests.get(nasa_api)
        data = response.json()
        image_url = data["url"]

        image_response = requests.get(image_url)
        explanation = data["explanation"]

        woeid = 2282863

        trends = api.trends_place(id = woeid)

        tags = ""
        count = 0
        for value in trends:
            for trend in value['trends']:
                if trend['name'][0] == '#':
                    tags += trend['name'] + " "
                    count += 1
                if count > 5:
                    break
        exp = ''
        for char in explanation:
            if char == '.':
                break
            else:
                exp += char
        tweet = exp + '''.

''' + tags

        image_path = "image.png"
        with open(image_path, 'wb') as img:
                img.write(image_response.content)
        
        status = api.update_with_media(image_path, tweet)

        posted = True

    if hour == 16 and minute == 10:
        posted = False
