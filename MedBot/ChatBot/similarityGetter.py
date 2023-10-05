import sys
import time
start = time.time()
if '--no-time' not in sys.argv:
    print("Loading similarityGetter.py...", end="\t")

import math
import re
from collections import Counter
from nltk.stem import WordNetLemmatizer


WORD = re.compile(r"\w+")

lematizer = WordNetLemmatizer()

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


def lematize_sentence(text):
    strfin = ""
    for word in text.split(" "):
        strfin += lematizer.lemmatize(word) + " "

    return strfin

def get_similarity(text1, text2):
    text1_lematized, text2_leamtized = lematize_sentence(text1), lematize_sentence(text2)
    vector1, vector2 = text_to_vector(text1_lematized), text_to_vector(text2_leamtized)
    return get_cosine(vector1, vector2)


end = time.time()
if '--no-time' not in sys.argv:
    print(f"Loaded similarityGetter.py in {round(end-start)/10}s")
