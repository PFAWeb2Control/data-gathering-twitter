require "rubygems"
require "json"
require "twitter"

cfg_file = open("../test-config.json")
# cfg_file = open("../config.json")
cfg = JSON.parse(cfg_file.read)

client = Twitter::Streaming::Client.new do |config|
  config.consumer_key        = cfg["consumer_key"]
  config.consumer_secret     = cfg["consumer_secret"]
  config.access_token        = cfg["access_token"]
  config.access_token_secret = cfg["access_secret"]
end

topics = ["Bordeaux"]
client.filter(track: topics.join(",")) do |object|
  if object.is_a?(Twitter::Tweet)
      puts "#{object.text}\n\t-> #{object.created_at} - #{object.favorite_count}♥ #{object.retweet_count}٭"

      if object.hashtags?
          object.hashtags.each do |hash|
              puts "#{hash.text}"
          end
      end
  end
end
