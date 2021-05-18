from utils import compute_score, contains_keywords, makePipeline, load_words
import json
import re


def tweet_to_json(tweet, i):
    tweet = re.sub("}},(\r|\n)+", "}}", tweet)
    tweet = re.sub('"source": "<a.*?>.*?</a>"', '"source":""', tweet)
    tweet = re.sub(r"}}]}$", "}}", tweet)
    tweet = json.loads(tweet)
    return tweet


def calc_score(content, keywords):
    matches = re.findall("|".join(keywords), content, flags=re.IGNORECASE)
    x = len(matches)
    if x == 0:
        return 0
    else:
        n_words = len(content.split())
        print(n_words)
        multiplier = (x*(x-1) + 1)
        print(multiplier)
        result = (x*(x-1) + 1)/n_words
        print(result)
        return result


def read_tweets(filename, words):
    """Reading in JSON data line by line.
    Print count of lines to the prompt"""
    total_tweets = 0
    with open(filename, "r") as file:
        for i, tweet in enumerate(file):
            try:
                data = tweet_to_json(tweet, i)
                tweet = data["value"]["properties"]["text"]
                # if contains_keywords(words, content=tweet):
                print(calc_score(tweet, words))
                # else: 
                #     print(calc_score(tweet, words))
                total_tweets += 1
                # if total_tweets == 5:
                #     break
            except ValueError as v:
                print("Malformed JSON in tweet ", i)
                print(v)
                print(tweet)
                # print()
    print(f"\nTotal tweets processed: {total_tweets}")
    return


def main():
    print("Start")

    fname_words = "climate.words"
    fname_data = "tinyTwitter.json"
    
    words = load_words(fname_words)
    read_tweets(fname_data, words)
    
    return


if __name__ == "__main__":
    main()
