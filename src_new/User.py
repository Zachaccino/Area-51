class User:
  def __init__(self):
    self.id = None
    self.visited = None
    self.depth = None
  
  def to_dict(self):
    return {
      "_id": self.id,
      "visited": self.visited,
      "depth": self.depth
    }
  
  def from_dict(self, d):
    self.id = d["_id"]
    self.visited = d["visited"]
    self.depth = d["depth"]
  
  