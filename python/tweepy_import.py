# coding: utf-8

from __future__ import unicode_literals
import json
import tweepy
import time

class MyStreamListener(tweepy.StreamListener):

    def __init__(self):
        tweepy.StreamListener.__init__(self)
        self.tweets = {"tweets":[]}

    def on_status(self, status):
        hashtags = []
        for h in status.entities["hashtags"]:
            hashtags += [h["text"]]

        self.tweets["tweets"] += [{"text": status.text, "hastags": hashtags}]

    def on_error(self, status_code):
        if status_code == 420:
            return False

    def show_tweets(self):
        tweets = json.dumps(self.tweets,indent=4 * ' ')
        self.tweets["tweets"] = []
        return tweets

def stream_filtered(criterias, interval=5, output_filepath="tweets.json", config_filepath="../config.json"):
    with open(config_filepath, 'r') as f:
        cfg = json.loads(f.read())

    auth = tweepy.OAuthHandler(cfg["consumer_key"], cfg["consumer_secret"])
    auth.set_access_token(cfg["access_token"], cfg["access_secret"])

    api = tweepy.API(auth)

    streamListener = MyStreamListener()
    stream = tweepy.Stream(auth = api.auth, listener=streamListener)
    stream.filter(track=criterias["track"], locations=criterias["locations"], async=True)

    while True:
        time.sleep(interval)
        print(streamListener.show_tweets())
