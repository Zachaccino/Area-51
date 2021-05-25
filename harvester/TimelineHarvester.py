"""
Jingyuan Tu (1232404), Melbourne, Australia
Floyd Everest-Dobson (664751), Melbourne, Australia
Bradley Schuurman (586088), Melbourne, Australia
Iris Li (875195), Melbourne, Australia
Paul Ou (888653), Melbourne, Australia
"""

import tweepy
import os
from utils import compute_score, contains_keywords, makePipeline, load_words, bounded_point, bounded_polygon
from TweetDatabase import TweetDatabase
from Tweet import Tweet
import time

class TimelineHarvester():
    def __init__(self, city_bboxes, wait_time=30):
        # {"City": Bounding Box}
        self.city_bboxes = city_bboxes
        # this is the time we should wait after harvesting all the tweets for all users.
        # in seconds
        self.wait_time = wait_time
        

    def start(self):
        print("Timeline Harvester Configuring...")

        # runtime parameters
        db_username = os.environ.get("DB_USERNAME")
        db_password = os.environ.get("DB_PASSWORD")
        db_address = os.environ.get("DB_ADDRESS")
        consumer_key = os.environ.get("CONSUMER_KEY")
        consumer_secret = os.environ.get("CONSUMER_SECRET_KEY")
        access_token = os.environ.get("ACCESS_TOKEN")
        access_secret = os.environ.get("ACCESS_TOKEN_SECRET")
        word_files = "filenames.txt"
        
        # connect database
        db = TweetDatabase()
        db.connect(db_username, db_password, db_address)
        db.setup()

        # connect tweeter api
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        api.verify_credentials()

        # load word metadata and process pipeline
        topic_keywords = {k: load_words(k) for k in load_words(word_files)}
        pipeline = makePipeline()

        print("Timeline Harvester Starting...")

        # mining loop
        while True:
            print("One Epoch Started...")
            # for each not yet visited user
            for user in db.get_all_users(visited=False):
                # for each of his/her's last 10 tweet
                for tweet in tweepy.Cursor(api.user_timeline, id=user.id, tweet_mode="extended").items(10):
                    if hasattr(tweet, "retweeted_status"):
                        try:
                            content = tweet.retweeted_status.extended_tweet["full_text"]
                        except:
                            content = tweet.retweeted_status.full_text
                    else:
                        try:
                            content = tweet.extended_tweet["full_text"]
                        except AttributeError:
                            content = tweet.full_text

                    location = None
                    bounding_box = None
                    city = None

                    # checks each city and if it is in one of them.
                    for city_name, city_bbox in self.city_bboxes.items():
                        # verify location.
                        if tweet.geo:
                            location = [tweet.geo["coordinates"][1], tweet.geo["coordinates"][0]] # [LONG, LAT]
                            if bounded_point(location, city_bbox):
                                city = city_name
                        
                        # verify bounding box.
                        if tweet.place and tweet.place.bounding_box and tweet.place.bounding_box.coordinates:
                            bounding_box = tweet.place.bounding_box.coordinates[0]
                            if bounded_polygon(bounding_box, city_bbox):
                                city = city_name

                        # located
                        if city:
                            break
                    
                    # if tweet not from city of interest, discard 
                    if not city: 
                        continue
                    
                    # ignore irrelevant tweets
                    if not contains_keywords(topic_keywords, content):
                        continue

                    # compute scores
                    n_words, n_vulgards, polarity, subjectivity, topic_scores = compute_score(pipeline, content, topic_keywords)
                    
                    user_id = None
                    if tweet.user:
                        user_id = tweet.user.id_str

                    tweetDto = Tweet()
                    tweetDto.id = tweet.id_str
                    tweetDto.content = tweet.full_text
                    tweetDto.coordinate = location
                    tweetDto.city = city
                    tweetDto.bounding_box = bounding_box
                    tweetDto.user_id = user_id
                    tweetDto.polarity = polarity
                    tweetDto.subjectivity = subjectivity
                    tweetDto.vulgard_count = n_vulgards
                    tweetDto.word_count = n_words
                    tweetDto.topic_scores = topic_scores

                    if db.add_tweet(tweetDto):
                        print(f"Tweet added {tweetDto.id}")
                
                # Update user as we've processed him.
                user.visited = True
                db.update_user(user)

            print("One Epoch Ended...")
            time.sleep(self.wait_time)