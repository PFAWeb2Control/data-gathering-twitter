#!/usr/bin/python2
# coding: utf-8
from __future__ import unicode_literals

"""
This example module shows how to use the various import libraries written for the project
"""

import time
from tweepy_import import FilteredStream



class MyFilteredStream(FilteredStream):
    """
    Custom filtered stream, looking for tweets from Bordeaux or mentioning Paris, and printing them in a formatted way
    """

    def __init__(self):
        """
        Construct a new custom stream
        :return: returns nothing
        """

        # Tweets from Bordeaux OR mentioning 'Paris'
        self.criterias = {
            "track": ['Paris'],
            "locations": [-0.6389644,44.8111222,-0.5334955,44.9163535]
        }
        FilteredStream.__init__(self, self.criterias, "../config.json")

    def action(self, tweets_list):
        """
        Override of FilteredStream.action()
        Print a formatted version of each tweet, with all of its informations

        :param tweets_list: list of tweets
        :return: returns nothing
        """
        for tweet in tweets_list :
            print("-> " + tweet["text"] + "\n\t-> " + str(tweet["date"]) + " - " + str(tweet["fav"]) + " ♥ " + str(tweet["rt"]) + " ٭ ")

            for h in tweet["hashtags"]:
                print("\t#" + h)

        print('---------------------------------------------\n')

stream = MyFilteredStream()
stream.stream(5, 5)
