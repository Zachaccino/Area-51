import tweepy
from config import create_api
import logging
# import database as db
import os
import pprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# COUCH_SERVER = "http://127.0.0.1:5984"
# USERNAME = os.environ.get("USERDB")
# PASSWORD = os.environ.get("PWDB")

"""

dict_keys(['created_at', 'id', 'id_str', 'full_text', 'truncated', 'display_text_range', 'entities', 'extended_entities', 'source', 
'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str', 'in_reply_to_screen_name', 'user', 
'geo', 'coordinates', 'place', 'contributors', 'is_quote_status', 'retweet_count', 'favorite_count', 'favorited', 'retweeted', 'possibly_sensitive', 'lang'])

"""

class TweetListener(tweepy.StreamListener):
    def __init__(self, api):  # did pass in api as an argument
        self.api = api

    # inherited from StreamListener class - overridden
    def on_status(self, tweet):
        # check if these are the coordinates for the bounding_box of Melbourne against Twitter docs 
        # [[[144.593741856, -38.433859306], [145.512528832, -38.433859306], [145.512528832, -37.5112737225], [144.593741856, -37.5112737225]]]
        bbox_melb = [144.70, -38.15, 145.40, -37.65]
        logger.info(f"Processing tweet id {tweet.id_str}")
        
        try:
            tweet_summary = self.get_tweet_summary(tweet)
            pprint(f"\n{tweet_summary}\n")
            print()
            # add tweet to database - returns True if successful 
            # self.db.add_data_to_db(tweet=tweet_summary, dbname=self.dbname)
            user_id = tweet_summary["user"]["id_str"]
            
            for status in tweepy.Cursor(self.api.user_timeline, id=user_id, tweet_mode="extended").items():
                user_tweet = status._json
                user_tweet_summary = self.get_user_tweet_summary(user_tweet)
                print(f"Tweet summary after processing \n\n {user_tweet_summary}")
                # print()
                # print(user_tweet_summary["coordinates"])
                if user_tweet_summary["coordinates"] is not None: 
                    # check if coordinates are in bbox_melb
                    print("\nIf loop\n")
                    print(user_tweet_summary["coordinates"]["coordinates"])
                    
                elif user_tweet_summary["place"]["bounding_box"]["coordinates"]:
                    print("\nElif loop\n")
                    print(user_tweet_summary["place"]["bounding_box"]["coordinates"])
                else:
                    pass
                # does the bounding_box for a profile 
                
                
        except BaseException as e:
            print(f"Error on data {e}\n")
            pass

        return True

    def get_tweet_summary(self, tweet):
    
        tweet_summary = {}

        # process User and Place objects
        tweet_user = self.get_user_attributes(tweet.user)
        tweet_place = self.get_place_attributes(tweet.place)

        tweet_summary["created_at"] = str(tweet.created_at)
        tweet_summary["id"] = tweet.id
        tweet_summary["_id"] = tweet.id_str
        tweet_summary["text"] = tweet.text
        tweet_summary["entities"] = tweet.entities
        tweet_summary["user"] = tweet_user
        tweet_summary["geo"] = tweet.geo
        tweet_summary["coordinates"] = tweet.coordinates
        tweet_summary["place"] = tweet_place
        tweet_summary["lang"] = tweet.lang

        return tweet_summary
    

    def get_user_attributes(self, user):
        """Take User object and extract important attributes"""
        user_profile = {}

        if user is not None:
            user_profile["id"] = user.id
            user_profile["id_str"] = user.id_str
            user_profile["name"] = user.name
            user_profile["screen_name"] = user.screen_name
            user_profile["location"] = user.location
            user_profile["description"] = user.description
            user_profile["geo_enabled"] = user.geo_enabled
            user_profile["lang"] = user.lang

        return user_profile

    def get_place_attributes(self, place):
        """Take Place object and extract important attributes"""
        place_attributes = {}
        bounding_box = {}
        if place is not None:
            # get attributes
            bounding_box["type"] = place.bounding_box.type
            bounding_box["coordinates"] = place.bounding_box.coordinates

            # convert to dictionary
            place_attributes["full_name"] = place.full_name
            place_attributes["url"] = place.url
            place_attributes["country"] = place.country
            place_attributes["place_type"] = place.place_type
            place_attributes["bounding_box"] = bounding_box

        return place_attributes


    def get_user_tweet_summary(self, tweet):
    
        tweet_summary = {}
        user = {}
        place = {}
        bbox = {}
        
        # User dictionary
        user["id"] = tweet["user"]["id"]
        user["_id"] = tweet["user"]["id_str"]
        user["name"] = tweet["user"]["name"]
        user["screen_name"] = tweet["user"]["screen_name"]
        user["location"] = tweet["user"]["location"]
        user["description"] = tweet["user"]["description"]
        user["geo_enabled"] = tweet["user"]["geo_enabled"]
        user["lang"] = tweet["user"]["lang"]

        # Place dictionary
        bbox["type"] = tweet["place"]["bounding_box"]["type"]
        bbox["coordinates"] = tweet["place"]["bounding_box"]["coordinates"]
        place["full_name"] = tweet["place"]["full_name"]
        place["place_type"] = tweet["place"]["place_type"]
        place["country"] = tweet["place"]["country"]
        place["bounding_box"] = bbox
        
        # Tweet summary
        tweet_summary["created_at"] = str(tweet["created_at"])
        tweet_summary["id"] = tweet["id"]
        tweet_summary["_id"] = tweet["id_str"]
        tweet_summary["text"] = tweet["full_text"]
        tweet_summary["entities"] = tweet["entities"]
        tweet_summary["user"] = user
        tweet_summary["geo"] = tweet["geo"]
        tweet_summary["coordinates"] = tweet["coordinates"]
        tweet_summary["place"] = tweet["place"]
        tweet_summary["lang"] = tweet["lang"]

        return tweet_summary


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

    def get_user_followers(self, num_followers):
        """Get followers from a given user return list of their followers."""
        print(self.twitter_user)
        followers = tweepy.Cursor(self.twitter_client.followers, self.twitter_user).items()
        for follower in followers:
            print(follower)
        # followers_list = [f for f in followers]
        print()
        # print(len(followers_list))
        print()
        return 


def main():

    api = create_api()

    # coordinates for the bounding_box: LONG/LAT (SW corner to NE corner)
    bounding_box_Melbourne = [144.70, -38.15, 145.40, -37.65]
    fetched_tweets_filename = "tweets_fetched.json"

    # should I be trying to get the tweet summary from the TweetListener class? 
    tweet_listener = TweetListener(api)
    stream = tweepy.Stream(api.auth, tweet_listener)
    stream.filter(locations=bounding_box_Melbourne)
    
    
    return


if __name__ == "__main__":
    main()