import re
from textblob import TextBlob
import spacy
from profanity_filter import ProfanityFilter

def contains_keywords(topic_keywords, content):
  for filename, keywords in topic_keywords.items():
    match = re.search("|".join(keywords), string=content, flags=re.IGNORECASE)
    if match:
      return True
  return False


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
def compute_score(pipeline, content, topic_keywords): 
  """
  topic_keywords: dictionary containing topics: words for computing topic scores. 
  Returns: topics and their associated score.
  
  """
  # profanity
  tokens = pipeline(content)
  content_doc = str(tokens)
  n_words = len(content_doc.split())
  n_vulgars = 0
  for t in tokens:
      n_vulgars += t._.is_profane
  # sentiment
  sentiment = TextBlob(content).sentiment
  # topic score
  topics = {}
  for filename in topic_keywords:
    # keywords becomes dictionary -> filename: list of keywords 
    keywords = topic_keywords[filename]
    topic_score = calc_score(content, keywords)
    topics[filename[:-4]] = topic_score
    # print(f"\nFilename is: {filename[:-4]}\nTopic score is: {topics[filename[:-4]]}\n")
  return n_words, n_vulgars, sentiment.polarity, sentiment.subjectivity, topics


def calc_score(content, keywords):
  matches = re.findall("|".join(keywords), content, flags=re.IGNORECASE)
  x = len(matches)
  if x == 0:
      return 0
  else:
      multiplied = x**2 - x + 1
      return multiplied


def load_words(fname):
  with open(fname, "r") as f:
      lines = f.readlines()
  words = []
  for l in lines:
      words.append(l.strip())
  return words


# bounds: pass in melb, syd etc.? 
def bounded_point(coordinates, bounds):
    x1_bound = bounds[0]
    y1_bound = bounds[1]
    x2_bound = bounds[2]
    y2_bound = bounds[3]
    x1 = coordinates[0] # longitude
    y1 = coordinates[1] # latitude
    if (x2_bound >= x1) and (x1 >= x1_bound) and (y2_bound >= y1) and (y1 >= y1_bound):
        return True
    return False


def bounded_polygon(polygon, bounds):
    x1_bound = bounds[0]
    y1_bound = bounds[1]
    x2_bound = bounds[2]
    y2_bound = bounds[3]
    x1 = polygon[0][0] # longitude
    y1 = polygon[0][1] # latitude
    x2 = polygon[1][0]
    y2 = polygon[2][1]
    if (x2_bound >= x1) and (x1 >= x1_bound) and (y2_bound >= y1) and (y1 >= y1_bound) and \
    (x2_bound >= x2) and (x2 >= x1_bound) and (y2_bound >= y2) and (y2 >= y1_bound):
        return True
    return False

  