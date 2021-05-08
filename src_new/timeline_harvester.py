import tweepy
from tweepy.models import User
from utils import compute_score, contains_keywords, makePipeline, load_words
from TweetDatabase import TweetDatabase
from pprint import pprint


# api info
api_key = "u32mQWX9oH5hCeGdNmTREqoyH"
api_secret = "kTyk9Y16Zcf7xcusErrviz97v754j4d76yx3rxj3gliOFpmpV8"
api_access = "2736973776-BLvoDsVFs07clTiIkeJi7mA9pYyKVhp8QI1gsPO"
api_access_secret = "iG1qveU6jUUtUkZVSFbSKG8CInqSrVZ5vwLYrDYsJ1ZgY"


# db info
db_username = "admin"
db_password = "pass"
db_address = "http://127.0.0.1:5984"
db = TweetDatabase()
db.connect(db_username, db_password, db_address)
db.setup()


# utils
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(api_access, api_access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


# search info
melb_bound = [144.593741856, -38.433859306, 145.512528832, -37.5112737225]
keywords = load_words("covid.words")
pipeline = makePipeline()


def bounded(coordinates, bounds):
  print(coordinates)
  print(bounds)
  x1_bound = bounds[0]
  y1_bound = bounds[1]
  x2_bound = bounds[2]
  y2_bound = bounds[3]
  x1 = coordinates[0] # longitude
  y1 = coordinates[1] # latitude
  if (x2_bound >= x1) and (x1 >= x1_bound) and (y2_bound >= y1) and (y1 >= y1_bound):
    return True
  return False


def fetch_timeline(user_id):
  for tweet in tweepy.Cursor(api.user_timeline, id=user_id, tweet_mode="extended").items():
    location = None
    if tweet.geo:
      location = [tweet.geo["coordinates"][1], tweet.geo["coordinates"][0]]
    else:
      print("LOCATION NONE")
      continue
    
    bouding_box = None
    if tweet.place and tweet.place.bounding_box:
      bouding_box = tweet.place.bounding_box.coordinates
    else:
      print("BOX NONE")
      continue

    if not bounded(location, melb_bound):
      print("GEO DENIED")
      continue
  
    if not bounded(bouding_box[0][0], melb_bound):
      print("BOX DENIED")
      continue
    
    # ignore irelevant tweets
    if not contains_keywords(keywords, tweet.full_text):
      return
    
    # compute scores
    n_words, n_vulgards, polarity, subjectivity = compute_score(pipeline, tweet.full_text)
    
    user_id = None
    if tweet.user:
      user_id = tweet.user.id_str

    print("Adding")

    tweetDto = Tweet()
    tweetDto.id = tweet.id_str
    tweetDto.content = tweet.full_text
    tweetDto.coordinate = location
    tweetDto.bounding_box = bouding_box
    tweetDto.user_id = user_id
    tweetDto.polarity = polarity
    tweetDto.subjectivity = subjectivity
    tweetDto.vulgard_count = n_vulgards
    tweetDto.word_count = n_words

    db.add_tweet(tweetDto)

screen_name = "DanielAndrewsMP"
id_str = "2213925990"
fetch_timeline(id_str)