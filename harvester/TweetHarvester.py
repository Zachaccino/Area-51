"""
Jingyuan Tu (1232404), Melbourne, Australia
Floyd Everest-Dobson (664751), Melbourne, Australia
Bradley Schuurman (586088), Melbourne, Australia
Iris Li (875195), Melbourne, Australia
Paul Ou (888653), Melbourne, Australia
"""

from TweetListener import TweetListener
import tweepy
from urllib3.exceptions import ProtocolError
import os


class TweetHarvester():
    def __init__(self, city_name, bbox):
        self.bbox = bbox
        self.city_name = city_name
    
    def start(self):
        print("Tweet Harvester Configuring...")
        db_username = os.environ.get("DB_USERNAME")
        db_password = os.environ.get("DB_PASSWORD")
        db_address = os.environ.get("DB_ADDRESS")
        consumer_key = os.environ.get("CONSUMER_KEY")
        consumer_secret = os.environ.get("CONSUMER_SECRET_KEY")
        access_token = os.environ.get("ACCESS_TOKEN")
        access_secret = os.environ.get("ACCESS_TOKEN_SECRET")
        word_files = "filenames.txt"

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        api.verify_credentials()

        tweet_listener = TweetListener(api, db_username, db_password, db_address, word_files, self.city_name, self.bbox)
        stream = tweepy.Stream(api.auth, tweet_listener)
        print("Tweet Harvester Configured...")

        while True:
            try:
                print("Harvesting...")
                stream.filter(locations=self.bbox)
            except ValueError as e:
                print(f"Tweet Harvester Value Error: {e}")
                continue
            except ProtocolError as e:
                print(f"Tweet Harvester Protocol Error: {e}")
                continue


