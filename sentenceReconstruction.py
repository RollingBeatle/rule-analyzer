from gensim import corpora, models, matutils
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import json
# import spacy
# import pyLDAvis
# import pyLDAvis.gensim
from pprint import pprint
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer


nltk.download('stopwords')
nltk.download('punkt')
categories = ["Other Indications","Safety","Road signs", "Weather",
               "Wildlife ", "Accident Response", "Emergency Driving Response",
                "Pedestrian/cyclist Interactions", "Interaction between vehicles", "Law enforcement interactions",
                 "Mechanical issues", "Emergency vehicles interactions", "Sanctions", "Substances", "DMV" ]

def main():
    categoryResultsDic = {}
    #Loading the set from the excel
    df = pd.read_excel('./data/Driving_Rules_October26.xlsx', sheet_name="Rules", engine="openpyxl")
    catTopics = separateByCategories(df)
    print(catTopics[0]['Natural Language Sentence'])
    print("-----------------------------")
    for index in range(len(catTopics)):
        natLang = catTopics[index]['Natural Language Sentence']
        #pprint(natLang)
        #Getting the stop words to remove from the ruleset
        stop_words = set(stopwords.words('english'))
        #Cleaning and tokenize
        cleanedWords = [word_tokenize(doc.lower()) for doc in natLang]
        cleanedWords = [[word for word in doc if word.isalnum() and word not in stop_words] for doc in cleanedWords]

        #pprint(cleanedWords)

        #corpus 
        dictionary = corpora.Dictionary(cleanedWords)
        corpus = [dictionary.doc2bow(doc) for doc in cleanedWords]

        #LDA model

        modelLDA = models.LdaModel(corpus, num_topics=3, id2word= dictionary)

        document_topics = [modelLDA[doc] for doc in corpus]
        print("the topics............................")
        pprint(document_topics)
        # Calculate transition probabilities based on topic distributions
        transition_matrix = np.zeros((modelLDA.num_topics, modelLDA.num_topics))

        for doc_topics in document_topics:
            for i, (topic_id, prob) in enumerate(doc_topics):
                if i + 1 < len(doc_topics):
                    next_topic_id, next_prob = doc_topics[i + 1]
                    transition_matrix[topic_id][next_topic_id] += prob * next_prob

        # Normalize transition probabilities
        row_sums = transition_matrix.sum(axis=1, keepdims=True)
        transition_matrix = np.where(row_sums == 0, 1 / modelLDA.num_topics, transition_matrix / row_sums)

        initial_topic = np.random.randint(modelLDA.num_topics)  # Choose a random initial topic
        num_steps = 5
        sampled_sequence = sample_from_markov_chain(initial_topic, transition_matrix, num_steps, modelLDA)
        print("Sampled Topic Sequence:", sampled_sequence)
        currentTopicList = []
        for topic_id in sampled_sequence:
            pprint(modelLDA.print_topic(topic_id))
            print('***************')
            currentTopicList.append(modelLDA.print_topic(topic_id))
        categoryResultsDic[categories[index]] = currentTopicList
    for key, value in categoryResultsDic.items():
        pprint(f"{key}: {json.dumps(value)}")
        print('-'*500)



def cleaningAndTokenizing(df:pd.DataFrame):
    
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

    return tokenized_sentences

def convertToNumberModel(processedDocs):
    #Create vectorizer
    #vectorizer = CountVectorizer()
    #Fit the text into a vector
    #X = vectorizer.fit_transform(processedDocs)
    dictionary = corpora.Dictionary(processedDocs)
    corpus = [dictionary.doc2bow(doc) for doc in processedDocs]
    #corpus = [doc.split() for doc in processedDocs]
    
    #corpus = matutils.Sparse2Corpus(X, documents_columns=False)
    
    #model
    lda_model = models.LdaModel(corpus, id2word=dictionary, num_topics=16, passes=10)

    #Extract Document Topics
    document_topics = [lda_model.get_document_topics(doc) for doc in corpus]
    pprint(document_topics)
    transitionMatrix(lda_model, document_topics)
    pprint(lda_model.print_topics())

def transitionMatrix(model, topics):

    topicNum = model.num_topics
    print(topicNum)
    transitionMtx = np.zeros((topicNum, topicNum))
    for doc_topics in topics:
        for i, j in zip(doc_topics[:-1], doc_topics[1:]):
            transitionMtx[i[0]][j[0]] += 1

    # Normalize transition matrix
    row_sums = transitionMtx.sum(axis=1, keepdims=True)
    #row_sums[row_sums == 0] = 1
    transitionMtx = np.where(row_sums == 0, 1 / topicNum, transitionMtx / row_sums)
    #transitionMtx/=row_sums

    # Print the transition matrix
    print("Transition Matrix:")
    pprint(transitionMtx)
    initial_topic = np.random.randint(topicNum)  # Choose a random initial topic
    num_steps = 5
    sampled_sequence = sample_from_markov_chain(initial_topic, transitionMtx, num_steps, model)
    print("Sampled Topic Sequence:", sampled_sequence)
    currentTopicList = []
    for topic_id in sampled_sequence:
        pprint(model.print_topic(topic_id))
        print('***************')
        currentTopicList.append(model.print_topic(topic_id))
    # categoryResultsDic[categories[index]] = currentTopicList
    # for key, value in categoryResultsDic.items():
    #     pprint(f"{key}: {json.dumps(value)}")
    #     print('-'*500)



def sample_from_markov_chain(initial_topic, transition_matrix, num_steps, modelLDA):
    current_topic = initial_topic
    sampled_topics = [current_topic]

    for _ in range(num_steps):
        current_topic = np.random.choice(modelLDA.num_topics, p=transition_matrix[current_topic])
        sampled_topics.append(current_topic)

    return sampled_topics

def separateByCategories(df:pd.DataFrame):
    separatedDFs = []

    for i in categories:
        filteredDf = df[df[i] == 1]
        separatedDFs.append(filteredDf)

    return separatedDFs 






if __name__ == "__main__":
    df = pd.read_excel('./data/Driving_Rules_October26.xlsx', sheet_name="Rules", engine="openpyxl")
    cleaned = cleaningAndTokenizing(df)
    convertToNumberModel(cleaned)
    #main()
