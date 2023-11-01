
from keras import Sequential, Model
from keras.layers import Dense, Embedding, LSTM, Bidirectional, Input, concatenate
import tensorflow as tf
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
from nltk.stem import WordNetLemmatizer
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from pprint import pprint
categories = ["Other Indications","Safety","Road signs", "Weather",
               "Wildlife ", "Accident Response", "Emergency Driving Response",
                "Pedestrian/cyclist Interactions", "Interaction between vehicles", "Law enforcement interactions",
                 "Mechanical issues", "Emergency vehicles interactions", "Sanctions", "Substances", "DMV" ]
def loadAndSeparateData():
    df = pd.read_excel('./data/Driving_Rules_October26.xlsx', sheet_name="Rules", engine="openpyxl")
    separatedDFs = []

    for i in categories:
        filteredDf = df[df[i] == 1]
        filteredDf = filteredDf.dropna(axis=1, how='all')
        filteredDf = filteredDf.loc[:, (df!=0).any(axis=0)]
        separatedDFs.append(filteredDf)

    return df, separatedDFs

def preprocessingData(df:pd.DataFrame):

    column_list = df['Natural Language Sentence'].tolist()
    #Tokenize
    tokenized_sentences = [word_tokenize(sentence) for sentence in column_list]
    #Lowercase
    tokenized_sentences = [[word.lower() for word in sentence] for sentence in tokenized_sentences]
    #Removing stopwords
    stop_words = set(stopwords.words('english'))
    tokenized_sentences = [[word for word in sentence if word not in stop_words] for sentence in tokenized_sentences]
    #lemmanization
    lemmatizer = WordNetLemmatizer()
    tokenized_sentences = [[lemmatizer.lemmatize(word) for word in sentence] for sentence in tokenized_sentences]

    pprint(tokenized_sentences)
    
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(column_list)
    pprint(tokenizer.word_docs)
    numerical_sentences = tokenizer.texts_to_sequences(tokenized_sentences)

    
    pprint(numerical_sentences)

def buildGenerator(totalWords, maxSequenceLenght):
    model = Sequential()
    #model.add(Dense(256, input_shape=))


def main():
    df, separated = loadAndSeparateData()
    print(separated[0])
    #preprocessingData(separated[0])



if __name__ == "__main__":
    main()
