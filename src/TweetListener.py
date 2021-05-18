from utils import compute_score, contains_keywords, makePipeline, load_words, bounded_point, bounded_polygon
import tweepy
from TweetDatabase import TweetDatabase
from Tweet import Tweet
from User import User
from pprint import pprint


# debug enables printing of tweet and scores
# dry_run disables database interaction
class TweetListener(tweepy.StreamListener):
    def __init__(self, api, db_username, db_password, db_address, fnames_keywords, bbox, debug=False):
        self.api = api
        self.pipeline = makePipeline()
        self.db = TweetDatabase()
        self.db.connect(db_username, db_password, db_address)
        self.db.setup()
        self.topic_keywords = {k: load_words(k) for k in load_words(fnames_keywords)}
        self.bbox = bbox
        self.debug = debug

    def on_status(self, tweet):
        if hasattr(tweet, "retweeted_status"):
            try:
                content = tweet.retweeted_status.extended_tweet["full_text"]
                # content = tweet.retweeted_status.extended_tweet.full_text
                # print("\n *** Try 1 *** \n")
            except:
                content = tweet.retweeted_status.text
                # print("\n *** Except 1 *** \n")
        else:
            try:
                content = tweet.extended_tweet["full_text"]
                # content = tweet.extended_tweet.full_text
                # print("\n *** Try 2 *** \n")
            except AttributeError:
                content = tweet.text
                # print("\n *** Except 2 *** \n")

        print(content)

        # ignore irrelevant tweets
        # if not contains_keywords(self.topic_keywords, content):
        #     return
        
        # compute scores
        n_words, n_vulgards, polarity, subjectivity, topic_scores = compute_score(self.pipeline, content, self.topic_keywords)

        location = None
        city = None
        if tweet.geo:
            # print(f"Tweet is: {tweet}\n")
            location = [tweet.geo["coordinates"][1], tweet.geo["coordinates"][0]] # [LONG, LAT]
            if bounded_point(location, self.bbox["melb"]):
                city = "melb"
                # print(f"Coordinates are {location} in {city}")
        
        if tweet.place.bounding_box.coordinates and not tweet.geo:
            bounding_box = tweet.place.bounding_box.coordinates[0]
            # print(f"Coordinates of bounding box are: {bounding_box}")
            if bounded_polygon(bounding_box, self.bbox["melb"]):
                city = "melb"
                # print(f"Bounding box: {city}")
            

        # Tweet Table 
        tweetDto = Tweet()
        tweetDto.id = tweet.id_str
        tweetDto.content = content
        tweetDto.coordinate = location
        tweetDto.city = city
        tweetDto.bounding_box = tweet.place.bounding_box.coordinates[0]
        tweetDto.user_id = tweet.user.id_str
        tweetDto.polarity = polarity
        tweetDto.subjectivity = subjectivity
        tweetDto.vulgard_count = n_vulgards
        tweetDto.word_count = n_words
        tweetDto.topic_scores = topic_scores
        tweetDto.lang = tweet.lang

        userDto = User()
        userDto.id = tweet.user.id_str
        userDto.visited = False
        userDto.depth = 0
        
        self.db.add_tweet(tweetDto)
        self.db.add_user(userDto)

        if self.debug:
            pprint(tweetDto.to_dict())
            pprint(userDto.to_dict())

        
    def on_error(self, status_code):
        if status_code == 420:
            print("Rate limit reached, terminating stream.")
            return False 
        else:
            print(f"Error Code: {status_code}.")
            return None