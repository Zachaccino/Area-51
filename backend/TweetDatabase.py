"""
Jingyuan Tu (1232404), Melbourne, Australia
Floyd Everest-Dobson (664751), Melbourne, Australia
Bradley Schuurman (586088), Melbourne, Australia
Iris Li (875195), Melbourne, Australia
Paul Ou (888653), Melbourne, Australia
"""

from Tweet import Tweet
from User import User
from cloudant.client import CouchDB
from cloudant.error import CloudantDatabaseException
from cloudant.design_document import DesignDocument
from cloudant.view import View


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

    # add views if they don't exist - customise them to the views we need 
    with DesignDocument(self.client[self.tweets_db_name], document_id="languages") as ddoc_tweets:
      def _add(view_name, view_key):
        if view_name not in ddoc_tweets.list_views():
          ddoc_tweets.add_view(view_name, "function (doc) { emit(doc.city, " + view_key + "); }", "_sum")
      def _add_subjectivity(view_name, view_key):
        if view_name not in ddoc_tweets.list_views():
          ddoc_tweets.add_view(view_name, "function(doc){if(" + view_key + ">0){emit(doc.city,doc.subjectivity);}}", "_sum")
      def _add_polarity(view_name, view_key):
        if view_name not in ddoc_tweets.list_views():
          ddoc_tweets.add_view(view_name, "function(doc){if(" + view_key + ">0){emit(doc.city,doc.polarity);}}", "_sum")
      def _add_counter(view_name, view_key):
        if view_name not in ddoc_tweets.list_views():
          ddoc_tweets.add_view(view_name, "function(doc){if(" + view_key + ">0){emit(doc.city,1);}}", "_sum")
      

      _add("vulgard", "doc.vulgard_count")
      _add("polarity", "doc.polarity")
      _add("subjectivity", "doc.subjectivity")
      _add("count", "doc.word_count")

      _add("covid", "doc.topic_scores.covid")
      _add_subjectivity("covid_subjectivity", "doc.topic_scores.covid")
      _add_polarity("covid_polarity", "doc.topic_scores.covid")
      _add_counter("covid_counter", "doc.topic_scores.covid")

      _add("climate", "doc.topic_scores.climate")
      _add_subjectivity("climate_subjectivity", "doc.topic_scores.climate")
      _add_polarity("climate_polarity", "doc.topic_scores.climate")
      _add_counter("climate_counter", "doc.topic_scores.climate")

      _add("finance", "doc.topic_scores.finance")
      _add_subjectivity("finance_subjectivity", "doc.topic_scores.finance")
      _add_polarity("finance_polarity", "doc.topic_scores.finance")
      _add_counter("finance_counter", "doc.topic_scores.finance")

      _add("housing", "doc.topic_scores.housing")
      _add_subjectivity("housing_subjectivity", "doc.topic_scores.housing")
      _add_polarity("housing_polarity", "doc.topic_scores.housing")
      _add_counter("housing_counter", "doc.topic_scores.housing")

      _add("sport", "doc.topic_scores.sport")
      _add_subjectivity("sport_subjectivity", "doc.topic_scores.sport")
      _add_polarity("sport_polarity", "doc.topic_scores.sport")
      _add_counter("sport_counter", "doc.topic_scores.sport") 


    with DesignDocument(self.client[self.users_db_name], document_id="user") as ddoc_users:
      if "depth" not in ddoc_users.list_views():
        ddoc_users.add_view("depth", "function (doc) { emit([doc.depth], 1);}", "_stats")
  
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
  
  # visited is None means get all users, True means get users that are visited
  # False means get users that are not visited.
  def get_all_users(self, visited=None):
    db = self.client[self.users_db_name]
    # generate user on the fly using yield
    for user_doc in db:
      try:
        user = User()
        user.from_dict(user_doc)
        if visited != None and user.visited != visited:
          continue
        yield user
      except Exception:
        # This is because design document is part of user database
        continue

  def update_tweet(self, tweet) -> bool:
    try:
      db = self.client[self.tweets_db_name]
      doc = db[tweet.id]
      doc["content"] = tweet.content
      doc["coordinate"] = tweet.coordinate
      doc["city"] = tweet.city
      doc["bounding_box"] = tweet.bounding_box
      doc["user_id"] = tweet.user_id
      doc["polarity"] = tweet.polarity
      doc["subjectivity"] = tweet.subjectivity
      doc["vulgard_count"] = tweet.vulgard_count
      doc["word_count"] = tweet.word_count
      doc["topic_scores"] = tweet.topic_scores
      doc["lang"] = tweet.lang
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


   # Get sentiment scores.
   # Possible views:
   # vulgard
   # polarity
   # subjectivity
   # count
   # covid
   # climate
   # finance
   # housing
   # sport
  def get_stats(self, view_name):
    try:
      with DesignDocument(self.client[self.tweets_db_name], "languages") as ddoc:
        result = {
          "sydney_1": 0,
          "sydney_2": 0,
          "melbourne_1": 0,
          "melbourne_2": 0
        }
        view = View(ddoc, view_name)
        with view.custom_result(group=True) as results:
          for r in results:
            result[r["key"]] = r["value"]
        return result
    except Exception:
      # Cannot find the view.
      return None
    