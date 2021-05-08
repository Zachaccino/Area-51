from utils import compute_score, contains_keywords, makePipeline, load_words
import tweepy
from TweetDatabase import TweetDatabase
from Tweet import Tweet
from User import User
from pprint import pprint


# debug enables printing of tweet and scores
# dry_run disables database interaction
class TweetListener(tweepy.StreamListener):
    def __init__(self, api, db_username, db_password, db_address, keywords_fname="covid.words", debug=False):
        self.api = api
        self.pipeline = makePipeline()
        self.db = TweetDatabase()
        self.db.connect(db_username, db_password, db_address)
        self.db.setup()
        self.keywords = load_words(keywords_fname)
        self.debug = debug

    def on_status(self, tweet):
        content = tweet.text

        # ignore irelevant tweets
        if not contains_keywords(self.keywords, content):
            return
        
        # compute scores
        n_words, n_vulgards, polarity, subjectivity = compute_score(self.pipeline, content)

        location = None
        if tweet.geo:
            location = tweet.geo.coordinates

        # Tweet Table 
        tweetDto = Tweet()
        tweetDto.id = tweet.id_str
        tweetDto.content = content
        tweetDto.coordinate = location
        tweetDto.bounding_box = tweet.place.bounding_box.coordinates
        tweetDto.user_id = tweet.user.id_str
        tweetDto.polarity = polarity
        tweetDto.subjectivity = subjectivity
        tweetDto.vulgard_count = n_vulgards
        tweetDto.word_count = n_words

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