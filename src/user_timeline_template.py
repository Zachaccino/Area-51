import tweepy
from config import create_api
import logging
# import database as db
# import os
# from pprint import pprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_user_tweet_summary(tweet):
    
        tweet_summary = {}
        user = {}
        place = {}
        bbox = {}

        # User dictionary
        if tweet["user"] is not None:
            user["id"] = tweet["user"]["id"]
            user["_id"] = tweet["user"]["id_str"]
            user["name"] = tweet["user"]["name"]
            user["screen_name"] = tweet["user"]["screen_name"]
            user["location"] = tweet["user"]["location"]
            user["description"] = tweet["user"]["description"]
            user["geo_enabled"] = tweet["user"]["geo_enabled"]
            user["lang"] = tweet["user"]["lang"]
        
        if tweet["place"] is not None:
            if tweet["place"]["bounding_box"] is not None:
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


def get_user_timeline(api, user_id):
    
    alltweets = []
    bbox_melb = [144.593741856, -38.433859306, 145.512528832, -37.5112737225]
    x1_melb, y1_melb, x2_melb, y2_melb = bbox_melb[0], bbox_melb[1], bbox_melb[2], bbox_melb[3]


    for status in tweepy.Cursor(api.user_timeline, id=user_id, tweet_mode="extended").items():
        user_tweet = status._json
        user_tweet_summary = get_user_tweet_summary(user_tweet)

        if user_tweet_summary["geo"] is not None:
            # print(user_tweet_summary)
            x1 = user_tweet_summary["geo"]["coordinates"][0] #LONG
            y1 = user_tweet_summary["geo"]["coordinates"][1] #LAT

            if (x2_melb >= x1) and  (x1 >= x1_melb) and (y2_melb >= y1) and (y1 >= y1_melb):
                # filter tweet and add to database
                # profanity/sentiment...
                print(f"Exact Coordinates: {x1, x2}") 
        elif user_tweet_summary["place"] is not None:
            coordinates = user_tweet_summary["place"]["bounding_box"]["coordinates"][0]
            x1 = coordinates[0][0]
            y1 = coordinates[0][1]
            x2 = coordinates[1][0]
            y2 = coordinates[2][1]

            if (x2_melb >= x1) and  (x1 >= x1_melb) and (y2_melb >= y1) and (y1 >= y1_melb):
                # filter tweet and add to database
                # profanity/sentiment...
                print(f"Bounding Box: {(x1, y1), (x2, y2)} ") 
        else: 
            continue

    return


def main():

    api = create_api()

    # fetch user id from database - iterate over users to 
    screen_name = "DanielAndrewsMP"
    id_str = "2213925990"

    get_user_timeline(api=api, user_id=id_str)

    return


if __name__ == "__main__":
    main()