import torch
import numpy as np
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from collections import Counter

def calculate_dist_n_score(text, n):
    tokens = word_tokenize(text)

    generated_ngrams = list(ngrams(tokens, n))
    
    unique_ngrams = len(set(generated_ngrams))
    
    total_ngrams = len(generated_ngrams)
    
    dist_n_score = unique_ngrams / total_ngrams if total_ngrams > 0 else 0.0
    return dist_n_score

def get_dist_n(dialogue='', n=1,):
    return calculate_dist_n_score(text=dialogue, n=n)
    
    
    