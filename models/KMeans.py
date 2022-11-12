import numpy as np 
import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from sklearn.metrics import silhouette_score


class K_Means:
    def __init__(self, data):
        self.data = data

    def vectorModel(self):
        word_features = self.data.get_feature_names()
        print(word_features)
        stemmer = SnowballStemmer('english')
        tokenizer = RegexpTokenizer(r'[a-zA-Z\']+')
    
    def KmeansModel(self, vector, clusterN):
        kmeans = KMeans(n_clusters = clusterN, n_init = 10)
        
        #print(self.data)
        self.fitted = kmeans.fit(self.data)
        
        words = vector.get_feature_names()
        common_words = kmeans.cluster_centers_.argsort()[:,-1:-11:-1]
        for num, centroid in enumerate(common_words):
            print(str(num) + ' : ' + ', '.join(words[word] for word in centroid))

    def elbowMeasure(self, rangeTest):
        clusterR = []
        for k in range(2,rangeTest):
            kmeans = KMeans(n_clusters=k, init="random", n_init=10, max_iter=300)
            kmeans.fit(self.data)
            score = kmeans.inertia_
            clusterR.append(score)
        return clusterR

    def silhoutteMeasure(self, rangeTest):
        clusterR = []
        for k in range(2,rangeTest):
            kmeans = KMeans(n_clusters=k, init="random", n_init=10, max_iter=300)
            kmeans.fit(self.data)
            score = silhouette_score(self.data, kmeans.labels_)
            clusterR.append(score)
        return clusterR    
    
