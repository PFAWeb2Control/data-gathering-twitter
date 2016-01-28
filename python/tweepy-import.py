# coding: utf-8

from __future__ import unicode_literals
import simplejson as json
import tweepy

with open('../test-config.json', 'r') as f:
    cfg = json.loads(f.read())

auth = tweepy.OAuthHandler(cfg["consumer_key"], cfg["consumer_secret"])
auth.set_access_token(cfg["access_token"], cfg["access_secret"])

api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
print myStream.filter(track=['Paris']).encode('utf-8').strip()
