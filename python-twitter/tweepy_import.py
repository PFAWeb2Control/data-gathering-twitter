"""
    A simple library to use even more easily Tweepy
"""

import simplejson as json
import tweepy

class FilteredStreamListener(tweepy.StreamListener):
    """
    FilteredStreamListener gather only some informations of each tweet
    """
    def __init__(self, fstream):
        """
        Construct a new 'FilteredStreamListener' object
        :return: returns nothing
        """
        tweepy.StreamListener.__init__(self)
        self.tweets = {"tweets":[]}
        self.fstream = fstream

    def on_status(self, status):
        """
        Tweets handling : select only some informations to keep and call
            FilteredStream.action() if enough tweets have been gathered

        :param status: a tweet
        :return: returns nothing
        """
        if status.lang in self.fstream.criterias["lang"] or status.lang == "und" or self.fstream.criterias["lang"][0] == "*":
            hashtags = []
            for h in status.entities["hashtags"]:
                hashtags += [h["text"]]

            self.tweets["tweets"] += [{ "text": status.text,
                                        "hashtags": hashtags,
                                        "author": status.user.name,
                                        "author_id": status.user.screen_name,
                                        "id": status.id_str,
                                        "date": str(status.created_at),
                                        "fav": status.favorite_count,
                                        "rt": status.retweet_count}]

            if(len(self.tweets["tweets"]) >= self.fstream.tweets_number):
                tweets = []
                for i in range(0, self.fstream.tweets_number):
                    tweets += [self.tweets["tweets"].pop(0)]

                self.fstream.action(tweets)

    def on_error(self, status_code):
        """
        Errors handling

        :param status_code: error code
        :return: False in case of an error (close the flux)
        """
        if status_code == 420:
            return False

class FilteredStream():
    """
    FilteredStream is a Twitter Stream filtered on multiple criterias
    """

    def __init__(self, criterias, tweets_number=10, config_filepath="../config.json"):
        """
        Construct a new 'FilteredStream' object

        :param criterias: dictionary containing keywords ("track"), location
            boundaries ("locations") and/or languages ("lang", using BCP 47
            language codes, or "*" to match any language), used to filter the
            search
        :param tweets_number: number of tweets between two calls to action()
            (default = 10 tweets)
        :param config_filepath: path to the JSON file containing the Twitter
            App's authentication informations
        :return: returns nothing
        """
        with open(config_filepath, 'r') as f:
            self.cfg = json.loads(f.read())

        self.auth = tweepy.OAuthHandler(self.cfg["consumer_key"], self.cfg["consumer_secret"])
        self.auth.set_access_token(self.cfg["access_token"], self.cfg["access_secret"])

        self.api = tweepy.API(self.auth)

        self.streamListener = FilteredStreamListener(self)
        self.liveStream = tweepy.Stream(auth = self.api.auth, listener=self.streamListener)

        self.criterias = criterias
        self.tweets_number = tweets_number

        self.tweets = []

    def action(self, tweets_list):
        """
        Perform an action on each set of tweets (by default, print the text of each tweet).
        Must be overidden.

        :param tweets_list: a list of tweets to treat
        """
        print("-> " + tweets_list["text"])

    def stream(self):
        """
        Start the Filtered Twitter Stream, and perform an action each X tweets

        :return: returns nothing (in fact, loops indefinitely)
        """

        self.liveStream.filter(track=self.criterias["track"], locations=self.criterias["locations"], async=True)

    def to_json(self, tweets):
        """
        Format tweets as JSON

        :param tweets: dictionary of tweets to format
        :return: returns the formatted tweets
        """
        # return json.dumps({"tweets": tweets}, sort_keys=True, indent=4 * ' ')
        return json.dumps({"tweets": tweets}, sort_keys=True)

    def export(self, filepath, tweets):
        """
        Prints tweets as JSON into a file (overwrite it)

        :param filepath: path to the output file
        :param tweets: dictionary of tweets to print as JSON
        :return: returns nothing
        """
        with open(filepath, 'w') as f:
            f.write(self.to_json(tweets))

        print(str(len(tweets)) + " tweets successfully exported to " + filepath)

class TwitterUser():
    """
    TwitterUser is a representation of Twitter's user
    """

    def __init__(self, pseudo, config_filepath="../config.json"):
        """
        Construct a new 'TwitterUser' object

        :param pseudo: string containing the user's pseudo (@something), also
            referred as 'screen_name' in the API
        :param config_filepath: path to the JSON file containing the Twitter
            App's authentication informations
        :return: returns nothing
        """

        with open(config_filepath, 'r') as f:
            self.cfg = json.loads(f.read())

        self.auth = tweepy.OAuthHandler(self.cfg["consumer_key"], self.cfg["consumer_secret"])
        self.auth.set_access_token(self.cfg["access_token"], self.cfg["access_secret"])

        self.api = tweepy.API(self.auth)

        self.user = self.api.get_user(pseudo)

    def tweets(self, nb=15):
        """
        Return a list of the last user's tweets

        :param nb: number of tweets to return
        !return: returns a list of tweets
        """
        return self.api.search(q="from:" + self.user.screen_name,count=5)
