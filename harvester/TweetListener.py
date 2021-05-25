from utils import compute_score, contains_keywords, makePipeline, load_words, bounded_point, bounded_polygon
import tweepy
from TweetDatabase import TweetDatabase
from Tweet import Tweet
from User import User


class TweetListener(tweepy.StreamListener):
    def __init__(self, api, db_username, db_password, db_address, fnames_keywords, city_name, bbox):
        self.api = api
        self.pipeline = makePipeline()
        self.db = TweetDatabase()
        self.db.connect(db_username, db_password, db_address)
        self.db.setup()
        self.topic_keywords = {k: load_words(k) for k in load_words(fnames_keywords)}
        self.city_name = city_name
        self.bbox = bbox
        
    def on_status(self, tweet):
        if hasattr(tweet, "retweeted_status"):
            try:
                content = tweet.retweeted_status.extended_tweet["full_text"]
            except:
                content = tweet.retweeted_status.text
        else:
            try:
                content = tweet.extended_tweet["full_text"]
            except AttributeError:
                content = tweet.text

        n_words, n_vulgards, polarity, subjectivity, topic_scores = compute_score(self.pipeline, content, self.topic_keywords)

        if not contains_keywords(self.topic_keywords, content) and n_vulgards == 0:
            return

        # check that all tweets from given bounding box actually come from that bounding box (and therefore correspond to the city)
        # some tweets will be harvested that have a bounding_box outside of city area 
        location = None
        bounding_box = None
        city = None
        if tweet.geo:
            location = [tweet.geo["coordinates"][1], tweet.geo["coordinates"][0]] # [LONG, LAT]
            if bounded_point(location, self.bbox):
                city = self.city_name
        
        if tweet.place and tweet.place.bounding_box and tweet.place.bounding_box.coordinates:
            bounding_box = tweet.place.bounding_box.coordinates[0]
            if bounded_polygon(bounding_box, self.bbox):
                city = self.city_name
        
        # if tweet not from city of interest, discard 
        if not city: 
            return

        tweetDto = Tweet()
        tweetDto.id = tweet.id_str
        tweetDto.content = content
        tweetDto.coordinate = location
        tweetDto.city = city
        tweetDto.bounding_box = bounding_box
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

        print(f"Tweet added {tweetDto.id}")
        print(f"User added {userDto.id}")
        
        
    def on_error(self, status_code):
        if status_code == 420:
            print("Rate limit reached, terminating stream.")
            return False 
        else:
            print(f"Error Code: {status_code}.")
            return None