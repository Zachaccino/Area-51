import tweepy
from config import create_api
from User import User
from TweetDatabase import TweetDatabase
import os


USERNAME = os.environ.get("USERDB")
PASSWORD = os.environ.get("PWDB")
COUCH_SERVER = "http://127.0.0.1:5984"


def get_followers(api, db, user_id, depth):
    """
    Get ids (strings) for each follower.
    count: gets the number of followers from each page (max = 5000)
    .pages(page_number): number of pages to request (15 max / 15 min period) 

    We only want to get 250 followers per user but request 500 to account for followers that might already be in the database. 
    """
    FOLLOWER_LIMIT = 250

    users_added = 0 
    num_followers = 250
    # page_number = 1
    
    for status in tweepy.Cursor(api.followers, screen_name=user_id, wait_on_rate_limit=True, count=num_followers, \
        tweet_mode="extended").items():
        # for usr in status: 
        # for i in range(len(status)):
            #id_str = status[i]._json["id_str"]
        id_str = status.id_str
        print(id_str)
        
        # create User object for couchDB 
        userDto = User()
        userDto.id = id_str
        userDto.visited = False
        userDto.depth = depth + 1

        # add user to database
        if db.add_user(userDto):
            users_added += 1
            print(f"User number {users_added} added.")
        
        if users_added == FOLLOWER_LIMIT:
            break
            
        print(users_added)

    # fetch user to update visited - update outside of for loop once done
    # user = db.get_user(id=user_id)
    # user.visited = True
    # db.update_user(user)
    
    return 
    
     
def main():

    api = create_api()

    # initialise and connect to database 
    db = TweetDatabase()
    db.connect(USERNAME, PASSWORD, COUCH_SERVER)
    db.setup()

    # fetch user id from database - iterate over users to 
    # screen_name = "BradleySchuurm1"
    screen_name = "DanielAndrewsMP"
    # id_str = "2213925990"

    get_followers(api, db, screen_name, 1)

    return


if __name__ == "__main__":
    main()