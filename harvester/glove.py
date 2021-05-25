"""
Jingyuan Tu (1232404), Melbourne, Australia
Floyd Everest-Dobson (664751), Melbourne, Australia
Bradley Schuurman (586088), Melbourne, Australia
Iris Li (875195), Melbourne, Australia
Paul Ou (888653), Melbourne, Australia
"""

# Word Representation 

import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


embeddings_dict = {}


def find_closest_embeddings(embedding):
    def comparator(word):
        # print(embeddings_dict[word], embedding)
        # print(len(embeddings_dict[word]))
        # print(len(embedding))
        # print(word)
        # print()
        return spatial.distance.euclidean(embeddings_dict[word], embedding)
    return sorted(embeddings_dict.keys(), key=comparator)


def main():

    print("Start")
    

    with open("glove.6B.50d.txt", "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], "float32")
            if vector.size != 50:
                print(i)
                continue
            embeddings_dict[word] = vector

    print("Dictionary built")

    while True:
        word = input("Give me a word: ")
        print(find_closest_embeddings(embeddings_dict[word])[1:25])
        if word == "Stop!":
            break

    return


if __name__ == "__main__":
    main()