#!/usr/bin/python2
# coding: utf-8
from __future__ import unicode_literals

# This example script shows how to use the tweepy_import wrapper written for
# the project

from tweepy_import import FilteredStream
from tweepy_import import TwitterUser

config = "../config.json"

# An example using the TwitterUser class
user = TwitterUser('interior', config)

tweets = []
for t in user.tweets(5):
    tweets += [t.text]

# Prints a list of five tweets
for t in tweets:
    print t

# Another example, with the FilteredStream class
class MyFilteredStream(FilteredStream):
    # Custom filtered stream, looking for tweets from Bordeaux or mentioning
    # Paris, and printing them in a formatted way

    def __init__(self):
        # Tweets from Bordeaux OR mentioning 'Paris', in ANY language
        self.criterias = {
            "track": ["Paris"], # Keywords filter
            "locations": [-0.6389644,44.8111222,-0.5334955,44.9163535], # Bordeaux bounding box
            # "lang": ["fr", "en"] # In French OR English
            "lang": ["*"] # Any language
        }
        FilteredStream.__init__(self, self.criterias, 5, config)

    # We redefine the action() method, in order to treat our packs of tweets the
    # way we want.
    #
    # Here, we print them in a special way.
    def action(self, tweets_list):

        for tweet in tweets_list :
            # Formatted printing
            print("-> " + tweet["text"] + "\n\t-> " +
                str(tweet["date"]) + " - " +
                str(tweet["fav"]) + " ♥ " +
                str(tweet["rt"]) + " ٭ ")

            for h in tweet["hashtags"]:
                print("\t#" + h)

        print('\n---------------------------------------------')
        # Data export to JSON
        self.export('test.json',tweets_list)
        print('---------------------------------------------\n')

stream = MyFilteredStream()
stream.stream()
