#!/usr/bin/ruby

# This example script shows how to use the twitter-import wrapper written for
# the project

require "./twitter-import"

# Custom filtered stream, looking for tweets from Bordeaux or mentioning
# Paris, and printing them in a formatted way
class MyFilteredStream < FilteredStream

    # Print a tweet
    # (Useful for tests and debug)
    def self.print_tweet(tweet)
        puts "#{tweet['text']}\n\t-> #{tweet['date']} - #{tweet['fav']}♥ #{tweet['rt']}٭"

        tweet['hashtags'].each do |hash|
            puts "#{hash.text}"
        end

    end

    # We redefine the action() method, in order to treat our packs of tweets the
    # way we want.
    #
    # Here, we print them in a special way.
    def action(tweets_list)
        tweets_list.each do |t|
            MyFilteredStream::print_tweet(t)
        end

        puts "\n---------------------------------------------"
        # Data export to JSON
        self.export('test.json', tweets_list)
        puts "---------------------------------------------\n"
    end

    def initialize()
        keywords = {
            "tracks" => ["Paris"], # Containing 'Paris' keyword
            "locations" => [[-0.6389644,44.8111222,-0.5334955,44.9163535]], # Bordeaux bounding box
            "lang" => ["fr", "en"] # In French OR English
            # "lang": ["*"] # Any language
        }

        super(keywords, 2, "../config.json")
    end
end

fs = MyFilteredStream.new
fs.stream
