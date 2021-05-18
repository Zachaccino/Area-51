import tweepy
from tweepy.models import User
from utils import compute_score, contains_keywords, makePipeline, load_words
from TweetDatabase import TweetDatabase
from pprint import pprint
from config import create_api


# api info
# api_key = "u32mQWX9oH5hCeGdNmTREqoyH"
# api_secret = "kTyk9Y16Zcf7xcusErrviz97v754j4d76yx3rxj3gliOFpmpV8"
# api_access = "2736973776-BLvoDsVFs07clTiIkeJi7mA9pYyKVhp8QI1gsPO"
# api_access_secret = "iG1qveU6jUUtUkZVSFbSKG8CInqSrVZ5vwLYrDYsJ1ZgY"


# db info
# db_username = "admin"
db_username = "bjschuurman"
db_password = "pass"
db_address = "http://127.0.0.1:5984"
db = TweetDatabase()
db.connect(db_username, db_password, db_address)
db.setup()


# utils
# auth = tweepy.OAuthHandler(api_key, api_secret)
# auth.set_access_token(api_access, api_access_secret)
# api = tweepy.API(auth, wait_on_rate_limit=True)
api = create_api()

fnames_keywords = "filenames.txt"

# search info
melb_bound = [144.593741856, -38.433859306, 145.512528832, -37.5112737225]
# keywords = load_words("covid.words")
topic_keywords = {k: load_words(k) for k in load_words(fnames_keywords)}
# print(topic_keywords)
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


def fetch_timeline(user_id, topic_keywords):
  for tweet in tweepy.Cursor(api.user_timeline, id=user_id, tweet_mode="extended").items(10):
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
    if tweet.geo:
      location = [tweet.geo["coordinates"][1], tweet.geo["coordinates"][0]] # LONG, LAT 
    else:
      print("LOCATION NONE")
      continue
    
    bounding_box = None
    if tweet.place and tweet.place.bounding_box:
      bounding_box = tweet.place.bounding_box.coordinates[0]
    else:
      print("BOX NONE")
      continue

    if not bounded(location, melb_bound):
      print("GEO DENIED")
      continue
  
    if not bounded(bounding_box[0][0], melb_bound):
      print("BOX DENIED")
      continue
    
    # ignore irrelevant tweets
    if not contains_keywords(topic_keywords, content):
      continue
    
    # compute scores
    n_words, n_vulgards, polarity, subjectivity, topic_scores = compute_score(pipeline, content, topic_keywords)
    
    user_id = None
    if tweet.user:
      print(tweet.user)
      user_id = tweet.user.id_str

    print("Adding")

    tweetDto = Tweet()
    tweetDto.id = tweet.id_str
    tweetDto.content = tweet.full_text
    tweetDto.coordinate = location
    tweetDto.bounding_box = bounding_box
    tweetDto.user_id = user_id
    tweetDto.polarity = polarity
    tweetDto.subjectivity = subjectivity
    tweetDto.vulgard_count = n_vulgards
    tweetDto.word_count = n_words
    tweetDto.topic_scores = topic_scores

    if db.add_tweet(tweetDto):
      print("Successfully added")

screen_name = "DanielAndrewsMP"
id_str = "2213925990"
fetch_timeline(id_str, topic_keywords)