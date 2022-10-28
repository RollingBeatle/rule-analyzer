import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

class WordBag:
    def __init__(self, data):
        self.data = data
        self.res = None
        self.clean = []
    def cleanData(self):
        for doc in self.data:
            self.clean[doc] = re.sub(r"[^a-zA-Z0-9]", " ", self.data[doc].lower()).split()
       
    def skImpl(self):
        vec = CountVectorizer (ngram_range=(2,2), stop_words="english")
        fitData = vec.fit_transform(self.data)
        df = pd.DataFrame(fitData.toarray(), columns=vec.get_feature_names())
        self.res = df
        print(df)


    