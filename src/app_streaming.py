from TweetListener import TweetListener
from config import create_api
import os
import tweepy
from urllib3.exceptions import ProtocolError
import time


USERNAME = os.environ.get("USERDB")
PASSWORD = os.environ.get("PWDB")
COUCH_SERVER = "http://127.0.0.1:5984"


def main():
    print("Starting App")
    melb_bound = {"melb": [144.593741856, -38.433859306, 145.512528832, -37.5112737225]}
    api = create_api()
    tweet_listener = TweetListener(api, USERNAME, PASSWORD, COUCH_SERVER, "filenames.txt", melb_bound, debug=False)
    stream = tweepy.Stream(api.auth, tweet_listener)

    while True:
        try:
            stream.filter(locations=melb_bound["melb"])
        except ValueError as e:
            print(f"Error: {e}")
            print("\n ************************************************ \n")
            # time.sleep(60)
            continue
        except ProtocolError as e:
            print(f"Error: {e}")
            print("\n ************************************************ \n")
            # time.sleep(60)
            continue


    # TODO: manage error being thrown when http/client.py throws: 
    # ValueError: invalid literal for int() with base 16: b''
    # urllib3.exceptions.ProtocolError: ('Connection broken: IncompleteRead(0 bytes read)', IncompleteRead(0 bytes read))
    # this is due to too much Twitter data being held in the background 

    print("Closing App")
    return


if __name__ == "__main__":
    main()

