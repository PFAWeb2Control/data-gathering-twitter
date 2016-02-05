#!/usr/bin/python
from tweepy_import import stream_filtered

# Tweets from Bordeaux OR mentioning 'Paris'
criterias = {
    "track": ['Paris'],
    "locations": [-0.6389644,44.8111222,-0.5334955,44.9163535]
    }

stream_filtered(criterias, 5, "tweets.json", "../test-config.json")
