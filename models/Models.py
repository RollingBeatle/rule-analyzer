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
        #defining punctuation and other symbols, stop words to be removed
        puncSigns = ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}',"%"]
        self.stop_words = text.ENGLISH_STOP_WORDS.union(puncSigns)
    
    def tfidV(self, data):
        #Define the TfidV and set to bigrams, determine the importance of the term
        vectorizer = TfidfVectorizer(stop_words = self.stop_words,use_idf=True, ngram_range=(2,2)) #Check smooth parameter?

        matrix = vectorizer.fit_transform(data)
        #saving vector for other models
        self.tfidVector  = matrix
        #transform to dataFrame to show in pandas representation
        tfDataFrame = pd.DataFrame(matrix.toarray(), columns=vectorizer.get_feature_names())
        #pca = SparsePCA(n_components=2).fit(X.toarray())
        #pca2d = pca.transform(X.toarray())
        return tfDataFrame
    
    def kmeans(self, data, clusterN):
        kmeans = KMeans(n_clusters = clusterN, n_init = 10)
        
        #print(self.data)
        self.fitted = kmeans.fit(self.data)
        
        words = vector.get_feature_names()
        common_words = kmeans.cluster_centers_.argsort()[:,-1:-11:-1]
        for num, centroid in enumerate(common_words):
            print(str(num) + ' : ' + ', '.join(words[word] for word in centroid))

    def svm (self, data):
        pass

    def elbowMeasure(self, rangeTest, data):
        clusterR = []
        for k in range(2,rangeTest):
            kmeans = KMeans(n_clusters=k, init="random", n_init=10, max_iter=300)
            kmeans.fit(data)
            score = kmeans.inertia_
            clusterR.append(score)
        return clusterR

    def silhoutteMeasure(self, rangeTest, data):
        clusterR = []
        for k in range(2,rangeTest):
            kmeans = KMeans(n_clusters=k, init="random", n_init=10, max_iter=300)
            kmeans.fit(self.data)
            score = silhouette_score(data, kmeans.labels_)
            clusterR.append(score)
        return clusterR
