import tweepy
import os
import logging


logger = logging.getLogger()


def create_api():
    """Create API object for credentials supplied.
    Return api object."""

    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET_KEY")
    access_token = os.environ.get("ACCESS_TOKEN")
    access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

    # OAuth - Authenticate to Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # we'll wait if the rate limit is exceeded
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    try:
        # returns object of class User
        user = api.verify_credentials()
        if user:
            print("Authentication OK")
            return api
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    # logger.info("API created")
