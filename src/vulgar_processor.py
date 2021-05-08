import sys
import re
import json
import time
import spacy
from profanity_filter import ProfanityFilter
from textblob import TextBlob

# need to run: python -m spacy download en 

def main():

    startTime = time.time()
    if len(sys.argv) != 2:
        print("Incorrect number of command-line arguments")
    filename = sys.argv[1]

    load_json(filename)

    print("--- %s seconds ---" % (time.time() - startTime))

    return


def tweet_to_json(tweet, i):

    tweet = re.sub("}},(\r|\n)+", "}}", tweet)
    tweet = re.sub('"source": "<a.*?>.*?</a>"', '"source":""', tweet)
    tweet = re.sub(r"}}]}$", "}}", tweet)
    tweet = json.loads(tweet)

    return tweet


def load_json(filename):
    """Reading in JSON data line by line.
    Print count of lines to the prompt"""

    total_tweets = 0

    with open(filename, "r") as file:
        vulgar = {}
        for i, tweet in enumerate(file):
            try:
                tweet = tweet_to_json(tweet, i)
                tweet_id = str(tweet["id"])
                text = tweet["value"]["properties"]["text"]
                filter_tweet_covid(tweet=text)
                # sentiment = compute_sentiment(text)
                # print()
                # vulgar_word_count = process_profanity_tweet(tweet=text)
                # tweet_length = count_tweet_length(tweet=text)
                # vulgar[tweet_id] = {
                #     "vulgar_words": vulgar_word_count,
                #     "tweet_length": tweet_length
                # }

                total_tweets += 1
                # if total_tweets == 5:
                #     # print(vulgar)
                #     break
            except ValueError as v:
                print("Malformed JSON in tweet ", i)
                print(v)
                print(tweet)
                # print()
    print(f"Total tweets processed: {total_tweets}")

    return

def count_tweet_length(tweet):

    nlp = spacy.load('en')
    doc = nlp(tweet)
    # print(f"Doc length is: {len(doc)}")
    new_doc = str(doc)
    # split_string = new_doc.split()
    tweet_length = len(new_doc.split())
    
    return tweet_length


def process_profanity_tweet(tweet):
    """Compute profanity score for each tweet.
    Think about selecting only those tweets with lang = "en" from Twitter? 
    """
    nlp = spacy.load('en')
    profanity_filter = ProfanityFilter(nlps={"en":nlp})
    # overrides the existing dictionary - is there a way to add to it?
    # profanity_filter.custom_profane_word_dictionaries = {"en": {"arsey", "cunty"}}
    nlp.add_pipe(profanity_filter.spacy_component, last=True)
    doc = nlp(tweet)
    # print(f'Tweet is: {tweet}')
    # print(f"Is it profane?: {doc._.is_profane}\n")
    
    vulgar_word_count = 0
    for token in doc:
        if token._.is_profane:
            vulgar_word_count += 1
    # print(vulgar_word_count)

    return vulgar_word_count


def compute_sentiment(tweet):
    sentiment = TextBlob(tweet).sentiment
    polarity = sentiment.polarity
    subjectivity = sentiment.subjectivity
    print(f"Polarity: {polarity};  Subjectivity: {subjectivity}")
    return sentiment

def filter_tweet_covid(tweet):
    keywords = ["covid", "covid-19", "covid19", "covid 19", "vaccine", "vaccination", "pfizer", "astrazeneca", "astra zeneca"]
    match = re.search("|".join(keywords), string=tweet, flags=re.IGNORECASE)
    if match:
        print("Match")
    return

if __name__ == "__main__":
    main()



#def filter_tweet_covid(tweet):
#    # print(tweet)
#    keywords = ["covid", "covid-19", "covid19", "covid 19", "vaccine", "vaccination", "pfizer", "astrazeneca", "astra zeneca"]
#    # match = re.search("covid", tweet, flags=re.IGNORECASE)
#    match = re.search("|".join(keywords), string=tweet, flags=re.IGNORECASE)
#    if match:
#        print("Match")
#    # matches = re.findall(pattern=r"[\w]+", string=tweet, flags=re.IGNORECASE)
#    # print(len(matches))
#    # print(matches)
#    # if any(w in keywords for w in re.findall(pattern=r"[\w]+", string=tweet, flags=re.IGNORECASE)):
#    #     print("Match")
#
#    return