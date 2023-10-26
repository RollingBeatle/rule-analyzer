from gensim import corpora, models
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import json

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
        print(natLang)
        #Getting the stop words to remove from the ruleset
        stop_words = set(stopwords.words('english'))
        #Cleaning and tokenize
        cleanedWords = [word_tokenize(doc.lower()) for doc in natLang]
        cleanedWords = [[word for word in doc if word.isalnum() and word not in stop_words] for doc in cleanedWords]

        print(cleanedWords)

        #corpus 
        dictionary = corpora.Dictionary(cleanedWords)
        corpus = [dictionary.doc2bow(doc) for doc in cleanedWords]

        #LDA model

        modelLDA = models.LdaModel(corpus, num_topics=3, id2word= dictionary)

        document_topics = [modelLDA[doc] for doc in corpus]
        print(document_topics)
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
            print(modelLDA.print_topic(topic_id))
            currentTopicList.append(modelLDA.print_topic(topic_id))
        categoryResultsDic[categories[index]] = currentTopicList
    for key, value in categoryResultsDic.items():
        print(f"{key}: {json.dumps(value)}")
        print('-'*500)

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
    main()
