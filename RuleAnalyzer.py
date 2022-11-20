import argparse
import logging
import os
from pydoc import doc
import pyfiglet
import pandas as pd
from models.WordBag import WordBag
from tools.GraphGen import GraphGen
import pandas as pd
from models.KMeans import K_Means

def openFile(filename):
    lines = []
    with open("./data/"+filename) as file:
        lines = [line.rstrip('\n') for line in file]
    return lines

def export(frame, name):
    frame.to_csv('./results/'+name+'.csv')

def compareDataFrameResults(dataSk, dataTf):
    sesumSk = dataSk.sum()
    sesumTF = dataTf.sum()
    dfsesumsk=pd.DataFrame({'apperances':sesumSk.values, 'word':sesumSk.index})
    dfsetf = pd.DataFrame({'apperances':sesumTF.values, 'word':sesumTF.index})

    arrayWordSK = dfsesumsk.iloc[:,1:].values
    arrayApSK = dfsesumsk.iloc[:,0].values
    arrayWordTF = dfsetf.iloc[:,1:].values
    arrayApTF = dfsetf.iloc[:,0].values


    print(arrayApSK)
    print(arrayWordSK)
    gp = GraphGen()
    gp.barGraph(arrayApSK,arrayWordSK, "Count-Vectorizer")
    gp.barGraph(arrayApTF,arrayWordTF, "Tfid-Vectorizer")
    gp.showResults()

    dfsumTf = dataTf.sum()
    print(dfsumTf)
    
def testData(data, wBag):

   vector,cleanedArray, pacp2d =  wBag.cleanData(data)
   model = K_Means(cleanedArray)
   model.KmeansModel(vector, 4)
   elbowData = model.elbowMeasure(100)
   silhoutteData = model.elbowMeasure(4)
   #GraphGen().lineGraphSingle(titleX="Number of Clusters", titleY="Error Elbow", rangeX=range(2,100), rangeY=elbowData)
   gp1 = GraphGen()
   gp1.lineGraphSingle(titleX="Number of Clusters", titleY="Error Silhouette", rangeX=range(2,4), rangeY=silhoutteData)
   print(cleanedArray)
   #gp1.spreadGraph(model.fitted.cluster_centers_,pacp2d)
   gp1.showResults()


def main():
    ascii_banner = pyfiglet.figlet_format("NLP Driving Rules Processor")
    print("#########################################################")
    print(ascii_banner)
    print("#########################################################")

    parser = argparse.ArgumentParser()
    parser.add_argument('--source', '-s', type=str, help='Name of source file')
    parser.add_argument('--csv', '-c', type=str, help='Name of file to save')
    parser.add_argument('--model', '-c', type=str, help='type of model to execute')
    args = parser.parse_args()

    option = input('Execute silhouette test, elbow test or none? (S,E,N)')
    document = openFile(args.source)

    document = openFile(args.source)
    print(document)
    args = parser.parse_args()

class Result:
    def __init__(self):
        pass

if __name__ == "__main__":

    ascii_banner = pyfiglet.figlet_format("NLP Driving Rules Processor")
    print("#########################################################")
    print(ascii_banner)
    print("#########################################################")

    parser = argparse.ArgumentParser()
    parser.add_argument('--source', '-s', type=str, help='Name of source file')
    parser.add_argument('--csv', '-c', type=str, help='Name of file to save')
    
    args = parser.parse_args()

    document = openFile(args.source)
    print(document)

    modelPL = WordBag(document)
    modelPL.tf_ldf(False)
    dfTf = modelPL.res
    modelPL.skImpl()

    dfsk = modelPL.res
    testData(document,modelPL)
    compareDataFrameResults(dfsk,dfTf)

    if args.csv:
        export(modelPL.res, args.csv)


