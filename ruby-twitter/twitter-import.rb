#!/usr/bin/ruby

# This is a simple example of wrapper for the Twitter Rubygem, using only the
# Twitter Streaming API
# Author::      Théo CHASSAIGNE (mailto:thchassa@enseirb-matmeca.fr)
# Copyright::   Copyright (c) 2016 Mnemosyne INRIA
# Licence::     (On its way)

require "rubygems"
require "json"
require "twitter"

class FilteredStream
    # Construct a new 'FilteredStream' object
    #
    # [criterias] hash containing keywords ("track"), location
    #     boundaries ("locations") and/or languages ("lang", using BCP 47
    #     language codes, or "*" to match any language), used to filter the
    #     search
    # [tweets_number] number of tweets between two calls to action()
    #     (default = 10 tweets)
    # [config_filepath] path to the JSON file containing the Twitter
    #     App's authentication informations
    # [return] returns nothing
    def initialize(criterias, tweets_number=10, config_filepath="../config.json")
        cfg_file = open(config_filepath)
        cfg = JSON.parse(cfg_file.read)

        @filter_max = tweets_number
        @criterias = criterias

        @client = Twitter::Streaming::Client.new do |config|
            config.consumer_key        = cfg["consumer_key"]
            config.consumer_secret     = cfg["consumer_secret"]
            config.access_token        = cfg["access_token"]
            config.access_token_secret = cfg["access_secret"]
        end
    end

    # Select only a few entries of a given tweet :
    #
    # * Its text
    # * The number of retweets
    # * The number of retweets
    # * The number of "likes"
    # * The creation date
    # * The hash of contained hashtags
    #
    # [t] tweet to filter
    #
    # [return] a filtered hash of a tweet
    def self.filter_tweet(t)
        hashtags = []
        if t.hashtags?
            t.hashtags.each do |hashtag|
                hashtags += [hashtag]
            end
        end

        tweet = {
            "text" => t.text,
            "rt" => t.retweet_count,
            "fav" => t.favorite_count,
            "date" => t.created_at,
            "hashtags" => hashtags
        }

        return tweet
    end

    # Format a given list of tweets to JSON
    # [tweets_list] hash of tweets to format
    # [return] JSON version a the tweets
    def self.to_json(tweets_list)
        info = { "tweets" => tweets_list }
        return info.to_json
    end

    # Perform an action on each set of tweets (by default, print the text of each tweet).
    # Should be overidden.
    #
    # [param tweets_list] a list of tweets to treat
    # [return] returns nothing
    def action(tweets_list)
        puts "-> " + t["text"]
    end


    # Start the Filtered Twitter Stream, and perform an action each X tweets
    #
    # [return] returns nothing (in fact, loops indefinitely)
    def stream()
        tweets_list = []

        @client.filter( track: @criterias["tracks"].join(","),
                        locations: @criterias["locations"].join(",")) do |object|
            if object.is_a?(Twitter::Tweet)
                unless  @criterias["lang"] != '*' and
                        not @criterias["lang"].include? object.lang
                    tweets_list += [FilteredStream::filter_tweet(object)]
                end
            end

            if tweets_list.length >= @filter_max
                action(tweets_list)
                tweets_list = []
            end
        end
    end

    # Print tweets as JSON into a file (overwrite it)
    #
    # [filepath] path to the output file
    # [tweets_list] dictionary of tweets to print as JSON
    # [return] returns nothing
    def export(filepath, tweets_list)
        output = File.open(filepath, "w")
        output.write(FilteredStream::to_json(tweets_list))
        output.close unless output.nil?

        puts "#{tweets_list.length} tweets successfully exported to #{filepath} !"
    end

end
