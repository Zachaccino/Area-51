"""
Jingyuan Tu (1232404), Melbourne, Australia
Floyd Everest-Dobson (664751), Melbourne, Australia
Bradley Schuurman (586088), Melbourne, Australia
Iris Li (875195), Melbourne, Australia
Paul Ou (888653), Melbourne, Australia
"""

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
  
  