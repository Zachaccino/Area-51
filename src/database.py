from cloudant.client import CouchDB
from cloudant.error import CloudantDatabaseException


class TwitterDatabase:
    """
    https://python-cloudant.readthedocs.io/en/stable/getting_started.html

    Steps:
    1. Construct the client
    2. Connect to the server 
    3. Perform tasks
    4. Disconnect from the server 

    """
    def __init__(self, username, password, server_url):
        self.username = username
        self.password = password
        self.url = server_url
        self.client = CouchDB(self.username, self.password, url=self.url, connect=True, auto_renew=True)

    def make_database(self, dbname, partitioned):
        """
        
        Create database if that database doesn't exist. 
        Partitioned databases introduce the ability for a user to create logical groups of documents 
        called partitions by providing a partition key with each document.
        
        """
        if partitioned:
            if dbname in self.client.all_dbs():
                print("Database already exists")
                return False
            else:
                try:
                    db = self.client.create_database(dbname, partitioned=True)
                    if db.exists():
                        print("Partitioned Success!")
                        return True
                except CloudantDatabaseException as e:
                    print(f"Error as {e}")
        else:
            if dbname in self.client.all_dbs():
                print("Database already exists")
                return False
            else:
                try: 
                    my_new_database = self.client.create_database(dbname)
                    if my_new_database.exists():
                        print("Success!")
                        return True
                except CloudantDatabaseException as e:
                    print(f"Error as {e}")


    def open_database(self, name):
        my_database = self.client[name]
        print(my_database)
        return True

    def delete_database(self, name):
        self.client.delete_database(name)
        if name in self.client.all_dbs():
            return False
        return True

    def add_data_to_db(self, tweet, dbname):
        """Inserts tweet into given database"""
        try:
            db = self.client[dbname]
            my_document = db.create_document(tweet, throw_on_exists=True)
            if my_document.exists():
                # print("Successfully added")
                return True
        except CloudantDatabaseException:
            # change this to pass if tweet already in database?
            # print("Tweet already in database")
            return False

