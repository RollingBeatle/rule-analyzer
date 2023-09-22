import pandas as pd
from nltk.tokenize import RegexpTokenizer
from collections import Counter
import argparse
import matplotlib.pyplot as plt
import seaborn as sns


from tabulate import tabulate
import nltk
from nltk.corpus import wordnet as wn
nltk.download('omw-1.4')

nltk.download('wordnet')
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--word', '-w', type=str, help='word to look into')
    parser.add_argument('--save', '-s', type=bool, help='save into csv')
    args = parser.parse_args()

    df = pd.read_csv("rules-csv-cols.csv")
    words = df[['Text','Rule','State']]
    tokenizer = RegexpTokenizer("[\w']+")
    wordSearch = args.word

    allRules = ' '.join(words['Rule'].tolist())
    tm = tokenizer.tokenize(allRules)

    allRulesText = ' '.join(words['Text'].tolist())
    tm1 = tokenizer.tokenize(allRulesText)

    #COUNTER WORDS FROM EXTRACTED RULES
    print("----------------------------- Words in the rules")
    Counterc = Counter(tm)
    most_occur = Counterc.most_common(2000)
    print(most_occur)
    print(type(most_occur[0][0]))

    #COUNTER WORDS FROM EXTRACTED TEXT
    print("----------------------------- Words in the natural language text")
    Counterc1 = Counter(tm1)
    most_occur1 = Counterc1.most_common(250)
    #print(most_occur1)

    dfWord = df[df['Rule'].str.contains(args.word)]
    dfWord.style
    #display(dfWord)
    print(tabulate(dfWord, headers='keys'))
    if args.save:
        dfWord.to_csv(args.word+'-rules.csv')
    pos_all = dict()
    for t in most_occur:
        pos_l = set()
        for tmp in wn.synsets(t[0]):
            
            if tmp.name().split('.')[0] == t[0]:
                pos_l.add(tmp.pos())
            elif t[0]== 'lights':
                print(t[0]+" - words - "+tmp.name())
        pos_all[t[0]] = pos_l
    print(pos_all)
    #print(type(pos_all))

    tupleList = []
    for tup in most_occur:
        newTup = (tup[0], tup[1], pos_all.get(tup[0]))
        tupleList.append(newTup)
    #print(tupleList)
    csvDataFrame = pd.DataFrame(tupleList, columns=["Word", "Frequency", "Type"])
    #print(csvDataFrame)
    csvDataFrame.to_csv("allWords.csv")
    while True:
        try:
            if wordSearch == 'end work':
                break
            elif wordSearch == 'graphs':
                plt.figure(figsize=(10,7))
                dfWords = pd.read_csv("rules-csv-cols.csv")
                for i in range(0,10):
                    plt.bar(names[i], data[i],  width=0.3 ) #label="$"+names[i]+"$",

                plt.legend()
                #plt.xlabel('Sampling type', fontsize=14)
                plt.xlabel('$Words$', fontsize=14)
                plt.xticks([])
                plt.title("$"+title+"$")
            wordSearch = str(input("New word to look for: \n"))
            newDF = df[df['Rule'].str.contains(wordSearch)]
            print(tabulate(newDF, headers='keys'))
        except ValueError:
            print("input a word")
        if wordSearch == 'end work':
            break


if __name__ == "__main__":
    main()