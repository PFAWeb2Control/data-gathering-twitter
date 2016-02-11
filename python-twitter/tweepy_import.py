# coding: utf-8
from __future__ import unicode_literals

"""
    A simple library to use even more easily Tweepy
"""

import simplejson as json
import tweepy
import time

class FilteredStreamListener(tweepy.StreamListener):
    """
    FilteredStreamListener gather only some informations of each tweet
    """
    def __init__(self):
        """
        Construct a new 'FilteredStreamListener' object
        :return: returns nothing
        """
        tweepy.StreamListener.__init__(self)
        self.tweets = {"tweets":[]}

    def on_status(self, status):
        """
        Tweets handling : select only some informations to keep

        :param status: a tweet
        :return: returns nothing
        """
        hashtags = []
        for h in status.entities["hashtags"]:
            hashtags += [h["text"]]

        self.tweets["tweets"] += [{ "text": status.text,
                                    "hashtags": hashtags,
                                    "date": status.created_at,
                                    "fav": status.favorite_count,
                                    "rt": status.retweet_count}]

    def on_error(self, status_code):
        """
        Errors handling

        :param status_code: error code
        :return: False in case of an error (close the flux)
        """
        if status_code == 420:
            return False

    def new_tweets(self):
        """
        Accessor on the Listener's tweets list

        :return: returns the list of new tweets since its last call
        """
        tweets = self.tweets["tweets"]
        self.tweets["tweets"] = []
        return tweets

class FilteredStream():
    """
    FilteredStream is a Twitter Stream filtered on multiple criterias
    """

    def __init__(self, criterias, config_filepath="../config.json"):
        """
        Construct a new 'FilteredStream' object

        :param criterias: dictionary containing keywords ("track") and/or location boundaries ("locations"), used to filter the search
        :param config_filepath: path to the JSON file containing the Twitter App's authentication informations
        :return: returns nothing
        """
        with open(config_filepath, 'r') as f:
            self.cfg = json.loads(f.read())

        self.auth = tweepy.OAuthHandler(self.cfg["consumer_key"], self.cfg["consumer_secret"])
        self.auth.set_access_token(self.cfg["access_token"], self.cfg["access_secret"])

        self.api = tweepy.API(self.auth)

        self.streamListener = FilteredStreamListener()
        self.liveStream = tweepy.Stream(auth = self.api.auth, listener=self.streamListener)
        self.criterias = criterias

        self.tweets = []

    def action(self, tweets_list):
        """
        Perform an action on each set of tweets (by default, print the text of each tweet).
        Must be overidden.

        :param tweets_list: a list of tweets to treat
        """
        print("-> " + tweets_list["text"])

    def stream(self, tweets_amount=10, interval=5):
        """
        Start the Filtered Twitter Stream, and perform an action each X tweets

        :param tweets_amount: number of tweets between two calls to action() (default = 10 tweets)
        :param interval: number of seconds between two recuperations of tweets (default = 5 seconds)

        :return: returns nothing (in fact, loops indefinitely)
        """

        self.liveStream.filter(track=self.criterias["track"], locations=self.criterias["locations"], async=True)

        while(True):
            while(len(self.tweets) < tweets_amount):
                time.sleep(interval)
                self.tweets += self.streamListener.new_tweets()

            tweets = []
            for i in range(0, tweets_amount):
                tweets += [self.tweets.pop(0)]

            self.action(tweets)
