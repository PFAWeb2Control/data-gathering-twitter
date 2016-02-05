# coding: utf8

from __future__ import unicode_literals
import json
import twitter

with open('../test-config.json', 'r') as f:
    cfg = json.loads(f.read())

api = twitter.Api(  consumer_key=cfg['consumer_key'],
                    consumer_secret=cfg['consumer_secret'],
                    access_token_key=cfg['access_token'],
                    access_token_secret=cfg['access_secret'])

api.VerifyCredentials()

for item in api.GetStreamFilter(track = 'Bordeaux', stall_warnings = True):
            print item['text'].encode('utf-8').strip()
