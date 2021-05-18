import tweepy
from TweetListener import TweetListener
import time 


# api info
api_key = "u32mQWX9oH5hCeGdNmTREqoyH"
api_secret = "kTyk9Y16Zcf7xcusErrviz97v754j4d76yx3rxj3gliOFpmpV8"
api_access = "2736973776-BLvoDsVFs07clTiIkeJi7mA9pYyKVhp8QI1gsPO"
api_access_secret = "iG1qveU6jUUtUkZVSFbSKG8CInqSrVZ5vwLYrDYsJ1ZgY"

# db info
db_username = "admin"
db_password = "pass"
db_address = "http://127.0.0.1:5984"

# utils
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(api_access, api_access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


# search info
melb_bound = [144.593741856, -38.433859306, 145.512528832, -37.5112737225]


myListener = TweetListener(api, db_username, db_password, db_address, debug=True)
myStream = tweepy.Stream(auth=auth, listener=myListener)

# Stream can be reused.
# But this call would stop when there's an error.
while True:
  try:
    myStream.filter(locations=melb_bound)
  except Exception:
    time.sleep(1000*60*5)
    