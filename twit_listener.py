import json
import pandas as pd
import tweepy
from tweepy.models import Status


class MyStreamListener(tweepy.StreamListener):
    """Custom Twitter Stream Listener class for this project
    """
    def __init__(self, hashtags_file, tweets_file, debug=False):
        """Initialization of class
        """
        self.hashtags_file = hashtags_file  # "./data/hashtags.csv"
        self.tweets_file = tweets_file  # "./data/tweets.csv"
        self.debug = debug

    def on_connect(self):
        """This is called after successfully connecting to the streaming API.
        """
        print("Connected to Stream")

    def on_status(self, status):
        """Extracts info from the tweet status
        """
        # Extract the tweet text from the various portions
        # (retweet, extended tweet, etc)
        tweet_text = ""
        if hasattr(status, "retweeted_status") and hasattr(
            status.retweeted_status, "extended_tweet"
        ):
            tweet_cat = "retweeted: "
            tweet_text = status.retweeted_status.extended_tweet["full_text"]
        if hasattr(status, "extended_tweet"):
            tweet_cat = "extended_tweet: "
            tweet_text = status.extended_tweet["full_text"]
        else:
            tweet_cat = "text: "
            tweet_text = status.text
        if self.debug:
            print(tweet_cat + tweet_text)

        # Only parse if the language is "English", we ignore other languages
        if status.lang == "en":
            # # START: Processing/Saving of the Hashtags # #
            # Parse the hashtags (those with a #<word>)
            hashtags_list = [
                x for x in tweet_text.replace("\n", " ").split(" ") if "#" in x
            ]

            # If there are any hashtags discovered
            if len(hashtags_list) == 0:
                pass
            else:
                # Open saved CSV file
                hashtags_pdf = pd.read_csv(self.hashtags_file, header=0)
                # Write/Update the count of the Hashtag
                for hashtag in hashtags_list:
                    if hashtag in list(hashtags_pdf["hashtag"]):
                        hashtags_pdf.loc[
                            (hashtags_pdf["hashtag"] == hashtag).index, "count"
                        ] += 1
                    else:
                        hashtags_pdf.loc[hashtags_pdf.shape[0]] = [hashtag, 1]
                # Save the CSV file
                hashtags_pdf.to_csv(self.hashtags_file, header=True, index=False)
            # # END: Processing/Saving of the Hashtags # #

            # # START: Saving of the Tweets/Hashtags # #
            # Open saved CSV file
            tweets_pdf = pd.read_csv(self.tweets_file, header=0)
            # Write the Tweet/Hashtag
            tweets_pdf.loc[tweets_pdf.shape[0]] = [
                tweets_pdf.shape[0],
                tweet_text,
                ";".join(hashtags_list),
            ]
            # Save the CSV file
            tweets_pdf.to_csv(self.tweets_file, header=True, index=False)
            # # END: Saving of the Tweets/Hashtags # #

    def on_data(self, raw_data):
        """The original streaming.py on_data method was causing errors
        """
        data = json.loads(raw_data)

        if "in_reply_to_status_id" in data:
            status = Status.parse(None, data)
            return self.on_status(status)
        if "delete" in data:
            delete = data["delete"]["status"]
            return self.on_delete(delete["id"], delete["user_id"])
        if "disconnect" in data:
            return self.on_disconnect_message(data["disconnect"])
        if "limit" in data:
            return self.on_limit(data["limit"]["track"])
        if "scrub_geo" in data:
            return self.on_scrub_geo(data["scrub_geo"])
        if "status_withheld" in data:
            return self.on_status_withheld(data["status_withheld"])
        if "user_withheld" in data:
            return self.on_user_withheld(data["user_withheld"])
        if "warning" in data:
            return self.on_warning(data["warning"])

    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            # returning False in on_error disconnects the stream
            print("Exiting listener")
            return False
