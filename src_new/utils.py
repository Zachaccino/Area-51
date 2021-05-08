import re
from textblob import TextBlob
import spacy
from profanity_filter import ProfanityFilter

def contains_keywords(keywords, content):
  match = re.search("|".join(keywords), string=content, flags=re.IGNORECASE)
  return True if match else False


# making a language processing pipeline.
# make one and only once, reuse it everytime, because it's very slow.
def makePipeline():
  nlp = spacy.load('en')
  pfilter = ProfanityFilter(nlps={"en":nlp})
  nlp.add_pipe(pfilter.spacy_component)
  return nlp


# need to download spacey
# python3 -m spacy download en
# Inspired by https://pypi.org/project/profanity-filter/#usage
def compute_score(pipeline, content):
  # profanity
  tokens = pipeline(content)

  n_vulgars = 0
  n_words = 0
  for t in tokens:
    n_vulgars += t._.is_profane
    n_words += 1
  
  # sentiment
  sentiment = TextBlob(content).sentiment
  return n_words, n_vulgars, sentiment.polarity, sentiment.subjectivity


def load_words(fname):
  with open(fname, "r") as f:
    lines = f.readlines()
  words = []
  for l in lines:
    words.append(l.strip())
  return words


  