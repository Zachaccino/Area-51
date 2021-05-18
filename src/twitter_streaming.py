import tweepy
from config import create_api
import logging
# import database as db
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# COUCH_SERVER = "http://127.0.0.1:5984"
# USERNAME = os.environ.get("USERDB")
# PASSWORD = os.environ.get("PWDB")

class TweetListener(tweepy.StreamListener):
    def __init__(self, filename):  # did pass in api as an argument
        self.api = create_api()
        self.filename = filename

    # inherited from StreamListener class - overridden
    def on_status(self, tweet):
        # logger.info(f"Processing tweet id {tweet.id}")
        tweet_summary = {}
        try:
            tweet_id = tweet.id
            tweet_id_str = tweet.id_str
            tweet_text = tweet.text
            tweet_geo = tweet.geo
            tweet_user = self.get_user_attributes(tweet.user)

            # writing attributes to dictionary
            tweet_summary["id"] = tweet_id
            tweet_summary["_id"] = tweet_id_str
            tweet_summary["text"] = tweet_text
            tweet_summary["geo"] = tweet_geo
            tweet_summary["user"] = tweet_user
            # tweet_out = json.dumps(tweet_summary)
            print(tweet_summary)
            # self.db.add_data_to_db(tweet=tweet_summary, dbname=self.dbname)
            # with open(self.filename, "a") as f:
            #    f.write(tweet_out + "\n")
            return True
        except BaseException as e:
            print(f"Error on data {e}")
            return False

    def get_user_attributes(self, user):
        """Take User object and create dictionary with important attributes"""
        user_profile = {}
        # get attributes from Status object
        user_id = user.id
        user_name = user.name
        user_screen_name = user.screen_name
        user_description = user.description

        # save attributes to dictionary
        user_profile["id"] = user_id
        user_profile["name"] = user_name
        user_profile["screen_name"] = user_screen_name
        user_profile["description"] = user_description

        return user_profile

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs
            return False
        logger.error(status)
        # print(status)
        return


class TwitterClient:
    """Different methods for different functionalities of the harvester.
    1. Get user timeline tweets"""

    def __init__(self, twitter_user=None):
        self.twitter_client = create_api()
        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        """Get tweets from users timeline and return list of tweets."""
        tweets = []
        for tweet in tweepy.Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets


class TwitterStreamer:

    def __init__(self,):
        self.api = create_api()

    def stream_tweets_keywords(self, streamed_tweets_filename, keywords):
        """This connects to the streaming Twitter API and streams tweets for keywords"""
        tweets_listener = TweetListener(streamed_tweets_filename)
        print(type(tweets_listener))
        stream = tweepy.Stream(self.api.auth, tweets_listener)
        stream.filter(track=keywords)
        return

    def stream_tweets_location(self, streamed_tweets_filename, location):
        """This connects to the streaming Twitter API and streams tweets for keywords"""
        tweets_listener = TweetListener(streamed_tweets_filename)
        # print(type(tweets_listener))
        stream = tweepy.Stream(self.api.auth, tweets_listener)
        stream.filter(locations=location)
        return


def main():

    # setup database
    # dbname = "twitter_data_docker"
    # my_database = db.TwitterDatabase(username=USERNAME, password=PASSWORD, server_url=COUCH_SERVER)
    # my_database.make_database(dbname=dbname, partitioned=False)

    # search_words = ["COVID-19", "COVID19", "COVID 19", "vaccine", "vaccination"]

    # coordinates for the bounding_box: LONG/LAT (SW corner to NE corner)
    bounding_box_Melbourne = [144.70, -38.15, 145.40, -37.65]
    fetched_tweets_filename = "tweets_fetched.json"

    # instantiate object of the class and start streaming
    # twitter_streamer = TwitterStreamer(dbname=dbname, db=my_database)
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets_location(fetched_tweets_filename, bounding_box_Melbourne)

    return


if __name__ == "__main__":
    main()