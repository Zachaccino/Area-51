"""
Jingyuan Tu (1232404), Melbourne, Australia
Floyd Everest-Dobson (664751), Melbourne, Australia
Bradley Schuurman (586088), Melbourne, Australia
Iris Li (875195), Melbourne, Australia
Paul Ou (888653), Melbourne, Australia
"""

class Tweet:
  def __init__(self):
    self.id = None
    self.content = None
    self.coordinate = None
    self.city = None
    self.bounding_box = None
    self.user_id = None
    self.polarity = None
    self.subjectivity = None
    self.vulgard_count = None
    self.word_count = None
    self.topic_scores = None
    self.lang = None
  
  # enforces database format
  # should have sanity checks but I'm too tired
  def to_dict(self):
    return {
      "_id": self.id,
      "content": self.content,
      "coordinate": self.coordinate,
      "city": self.city,
      "bounding_box": self.bounding_box,
      "user_id": self.user_id,
      "polarity": self.polarity,
      "subjectivity": self.subjectivity,
      "vulgard_count": self.vulgard_count,
      "word_count": self.word_count,
      "topic_scores": self.topic_scores,
      "lang": self.lang
    }
  
  # read data from a dict
  def from_dict(self, d):
    self.id = d["_id"]
    self.content = d["content"]
    self.coordinate = d["coordinate"]
    self.city = d["city"]
    self.bounding_box = d["bounding_box"]
    self.user_id = d["user_id"]
    self.polarity = d["polarity"]
    self.subjectivity = d["subjectivity"]
    self.vulgard_count = d["vulgard_count"]
    self.word_count = d["word_count"]
    self.topic_scores = d["topic_scores"]
    self.lang = d["lang"]