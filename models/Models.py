import numpy as np 
import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from sklearn.metrics import silhouette_score
from sklearn.feature_extraction import text
from sklearn.decomposition import SparsePCA

class Model: 

    def __init__(self):
        #defining punctuation and other symbols
        puncSigns = ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}',"%"]
        #stop words to be removed
        self.stop_words = text.ENGLISH_STOP_WORDS.union(puncSigns)
    
    def tfidV(self, data):

        vectorizer = TfidfVectorizer(stop_words = self.stop_words)
        X = vectorizer.fit_transform(data)
        pca = SparsePCA(n_components=2).fit(X.toarray())
        pca2d = pca.transform(X.toarray())
    
    def countV(self, data):
        pass
    
    def kmeans(self, data):
        pass

    def svm (self, data):
        pass
