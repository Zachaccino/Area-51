from Tweet import Tweet
from User import User
from cloudant.client import CouchDB
from cloudant.error import CloudantDatabaseException

# Couch DB Wrapper
class TweetDatabase:
  def __init__(self):
    self.client = None
    self.tweets_db_name = "tweets"
    self.users_db_name = "users"
    
  def connect(self, username, password, address):
    self.client = CouchDB(username, password, url=address, connect=True, auto_renew=True)

  def disconnect(self):
    self.client.disconnect()

  def setup(self):
    existing_dbs = self.client.all_dbs()
    if self.tweets_db_name not in existing_dbs:
      self.client.create_database(self.tweets_db_name)
    if self.users_db_name not in existing_dbs:
      self.client.create_database(self.users_db_name)
  
  # this is a Tweet object
  # return True on success, returns false on duplicate or unknown failure.
  def add_tweet(self, tweet) -> bool:
    try:
      db = self.client[self.tweets_db_name]
      db.create_document(tweet.to_dict(), throw_on_exists=True)
      return True
    except CloudantDatabaseException:
      return False
  
  # this is a User object
  # return True on success, returns false on duplicate or unknown failure.
  def add_user(self, user) -> bool:
    try:
      db = self.client[self.users_db_name]
      db.create_document(user.to_dict(), throw_on_exists=True)
      return True
    except Exception:
      return False
    
  
  # id_str of the tweet.
  def get_tweet(self, id):
    try:
      db = self.client[self.tweets_db_name]
      tweet = Tweet()
      tweet.from_dict(db[id])
      return tweet
    except Exception:
      return None

  def get_user(self, id):
    try:
      db = self.client[self.users_db_name]
      user = User()
      user.from_dict(db[id])
      return user
    except Exception:
      return None

  def update_tweet(self, tweet) -> bool:
    try:
      db = self.client[self.tweets_db_name]
      doc = db[tweet.id]
      doc["content"] = tweet.content
      doc["coordinate"] = tweet.coordinate
      doc["bounding_box"] = tweet.bounding_box
      doc["user_id"] = tweet.user_id
      doc["polarity"] = tweet.polarity
      doc["subjectivity"] = tweet.subjectivity
      doc["vulgard_count"] = tweet.vulgard_count
      doc["word_count"] = tweet.word_count
      doc.save()
      return True
    except Exception:
      return False

  def update_user(self, user) -> bool:
    try:
      db = self.client[self.users_db_name]
      doc = db[user.id]
      doc["visited"] = user.visited
      doc["depth"] = user.depth
      doc.save()
      return True
    except Exception:
      return False

  def remove_tweet(self, id):
    db = self.client[self.tweets_db_name]
    doc = db[id]
    doc.delete()

  def remove_user(self, id):
    db = self.client[self.users_db_name]
    doc = db[id]
    doc.delete()


    
  



  

  