#!/usr/bin/ruby

# The program is a simple example of how to use the Twitter Streaming API with the Twitter Rubygem
# Author::      Théo CHASSAIGNE (mailto:thchassa@enseirb-matmeca.fr)
# Copyright::   Copyright (c) 2016 Mnemosyne INRIA
# Licence::     (On its way)

require "rubygems"
require "json"
require "twitter"

# Print a tweet
# (Useful for tests and debug)
def print_tweet(tweet)
    puts "#{tweet.text}\n\t-> #{tweet.created_at} - #{tweet.favorite_count}♥ #{tweet.retweet_count}٭"

    if tweet.hashtags?
        tweet.hashtags.each do |hash|
            puts "#{hash.text}"
        end
    end
end

# Select only a few entries of a given tweet :
#
# * Its text
# * The number of retweets
# * The array of contained hashtags
#
def filter_tweet(t)
    hashtags = []
    if t.hashtags?
        t.hashtags.each do |hashtag|
            hashtags += [hashtag.text]
        end
    end

    tweet = {
        "text" => t.text,
        "retweet_count" => t.retweet_count,
        "hashtags" => hashtags
    }

    return tweet
end

# Parse tweets filtered with keywords during a given time,
# convert them to JSON format and put it in a file
#
# [keywords] an ARRAY of keywords used to filter the tweets
# [time] the number of seconds during which the script will run
# [output_filepath] the path to the output JSON file
# [config_filepath] the path to the application JSON config file
#
def stream_filtered(keywords, time=3600, output_filepath="tweets.json", config_filepath="../config.json")
    cfg_file = open(config_filepath)
    cfg = JSON.parse(cfg_file.read)

    client = Twitter::Streaming::Client.new do |config|
      config.consumer_key        = cfg["consumer_key"]
      config.consumer_secret     = cfg["consumer_secret"]
      config.access_token        = cfg["access_token"]
      config.access_token_secret = cfg["access_secret"]
    end

    output = File.open(output_filepath, "w")
    tweets = []

    t = Time.now
    t_end = t + time

    client.filter(track: keywords.join(",")) do |object|
      if object.is_a?(Twitter::Tweet)
          tweets += [filter_tweet(object)]
      end

      t = Time.now
      if t > t_end
          break # Yup, dirty, but client.filter() in a continuous ("infinite") loop...
      end
    end


    info = {
        "tweets" => tweets
    }

    output.write(info.to_json)
    output.close unless output.nil?
end

#stream_filtered(["Bordeaux", "Paris"], 5, "tweets.json", "../test-config.json")
