# This program checks the accuracy of sentiment analysis using textblob
import nltk
from nltk.corpus import twitter_samples
from textblob import TextBlob
nltk.download('twitter_samples')
# nltk has 5,000 manually classified positive and negative tweets.
# This can be used to varify textblob's accuracy
neg = twitter_samples.strings('negative_tweets.json')
pos = twitter_samples.strings('positive_tweets.json')
counter = 0
for i in neg:
	sentiment = TextBlob(i).polarity
	if sentiment < 0:
		counter = counter + 1
print("Negative Sentiment Accuracy: " + str(counter / len(neg) * 100) + "%")

counter = 0
for i in pos:
	sentiment = TextBlob(i).polarity
	if sentiment > 0:
		counter = counter + 1
print("Positive Sentiment Accuracy: " + str("%.2f" % (counter / len(neg) * 100)) + "%")