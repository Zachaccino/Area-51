from TweetDatabase import TweetDatabase
from cloudant.design_document import DesignDocument
from cloudant.view import View
from cloudant.query import Query
import os

USERNAME = os.environ.get("USERDB")
PASSWORD = os.environ.get("PWDB")
COUCH_SERVER = "http://127.0.0.1:5984"


def check_view(ddoc, view):
    with ddoc: 
        print(ddoc.list_views())
        if view not in ddoc.list_views():
            # ddoc.add_view(view, "function (doc) { emit([doc.topic_scores.sport.words], 1);}", "_stats")
            print(f"{view} not yet in database.")
        else:
            print(f"{view} already exists.")
    return 


def add_view_to_db(db, ddoc_name, view):
    with DesignDocument(database=db, document_id=ddoc_name) as ddoc:
        if view in ddoc.list_views(): 
            return False
        ddoc.add_view(view_name=view, map_func="function (doc) { emit([doc.word_count], 1);}", reduce_func="_sum")
    return True

def main():

    db = TweetDatabase()
    db.connect(USERNAME, PASSWORD, COUCH_SERVER)
    db.setup()
    # db.tweets_db_name
    database = db.client["tweets"]
    add_view_to_db(database, "language", "word_count")

    ddoc_tweets = DesignDocument(database=db.client["tweets"], document_id="language")
    view = View(ddoc_tweets, "word_count")

    for row in view(limit=10):
        print(type(row))
        print(row)

    # query = Query(database=database, selector={"word_count": {"$gt": 5}})
    # with query.custom_result(sort=[{"word_count": "desc"}]) as rslt:
    #     for doc in rslt:
    #         print(doc["polarity"])
    
    # ddoc_tweets = DesignDocument(database=db.client["tweets"], document_id="languages")
    # ddoc_user = DesignDocument(database=db.client["users"], document_id="user")
    
    # incorrect map function - below we override it, leaving reduce_func unchanged 
    # with ddoc: 
    #     ddoc.update_view(view_name="sport", map_func="function (doc) { emit([doc.subjectivity, doc.lang], 1);}")

    # check_view(ddoc_tweets, "vulgar")
    # check_view(ddoc_user, "depth")

    # override existing Map function 
    # with DesignDocument(database=db.client["tweets"], document_id="scores") as ddoc:
    #     ddoc.update_view(view_name="sport", map_func="function (doc) { emit([doc.polarity, doc.lang], 1);}")

    return


if __name__ == "__main__":
    main()







# 1394153812668022784

    # with DesignDocument(database=db.client["tweets"], document_id="languages") as ddoc:
    #     ddoc.add_view(view_name="language", map_func="function (doc) { emit([doc.lang], 1);}", reduce_func="_stats")

    # with DesignDocument(database=db.client["tweets"], document_id="languages") as ddoc:
    #     ddoc.add_view(view_name="words", map_func="function (doc) {doc.content.toLowerCase().split(/\W+/).forEach(function (word) \
    #      {if (word.length > 1) {emit([word, doc.lang], 1);}});}", reduce_func=
    #         """function (keys, values, rereduce) {var langs = []; var count = 0; if (!rereduce) {keys.forEach(function (key) \
    #         { var lang = key[0][1]; if (langs.indexOf(lang) < 0) {langs.push(lang);}count++;});} \
    #            else {values.forEach(function (value) {value.languages.forEach(function (lang) { if (langs.indexOf(lang) < 0) {langs.push(lang);} count += value.count; }); }); 
    #              }return {languages: langs, count: count};}""")