import json
import os
import pandas as pd
import tweepy
from twit_listener import MyStreamListener

if __name__ == "__main__":
    """#For easier debugging
    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""
    hashtags_file = "./data/hashtags.csv"
    tweets_file = "./data/tweets.csv"
    search_keyword = "python"
    """

    # Extract the configuration parameters from the config file
    config_file = "./config.json"
    with open(config_file, "r") as jsonfile:
        cfg = json.load(jsonfile)

    consumer_key = cfg["consumer_key"]
    consumer_secret = cfg["consumer_secret"]
    access_token = cfg["access_token"]
    access_token_secret = cfg["access_token_secret"]
    hashtags_file = cfg["hashtags_file"]
    tweets_file = cfg["tweets_file"]
    search_keyword = cfg["search_keyword"]

    # create the hashtags and tweets cache file if it doesn't exist
    if not os.path.exists(hashtags_file):
        hashtags_pdf = pd.DataFrame(columns=["hashtag", "count"])
        hashtags_pdf.to_csv(hashtags_file, header=True, index=False)
    if not os.path.exists(tweets_file):
        tweets_pdf = pd.DataFrame(columns=["index", "tweet", "hashtags"])
        tweets_pdf.to_csv(tweets_file, header=True, index=False)

    # Start the listener & collector
    myStreamListener = MyStreamListener(hashtags_file, tweets_file)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    myStream = tweepy.Stream(
        auth=auth, listener=myStreamListener, tweet_mode="extended"
    )
    myStream.filter(track=[search_keyword])
