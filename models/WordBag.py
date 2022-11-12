import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pandas as pd
from sklearn.feature_extraction import text
from sklearn.decomposition import SparsePCA

class WordBag:
    def __init__(self, data):
        self.data = data
        self.res = None
        self.clean = None
    def cleanData(self, toClean):
        puncSigns = ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}',"%"]
        stop_words = text.ENGLISH_STOP_WORDS.union(puncSigns)
        vectorizer = TfidfVectorizer(stop_words = stop_words)
        X = vectorizer.fit_transform(toClean)
        pca = SparsePCA(n_components=2).fit(X.toarray())
        pca2d = pca.transform(X.toarray())
        
        return vectorizer, X, pca2d
       
    def skImpl(self):
        vec = CountVectorizer (ngram_range=(2,2), stop_words="english")
        fitData = vec.fit_transform(self.data)
        df = pd.DataFrame(fitData.toarray(), columns=vec.get_feature_names())
        self.res = df
        print(df)

    def tf_ldf(self, smooth):
        tfDataVector = TfidfVectorizer(use_idf=True, smooth_idf=smooth, ngram_range=(2,2), stop_words='english')
        tfDataTransform = tfDataVector.fit_transform(self.data)
        tfDataFrame = pd.DataFrame(tfDataTransform.toarray(), columns=tfDataVector.get_feature_names())
        print(tfDataFrame)
        self.res = tfDataFrame

    