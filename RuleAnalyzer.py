import argparse
import logging
import os
from pydoc import doc
import pyfiglet
import pandas as pd
from tools.GraphGen import GraphGen
import pandas as pd
from models.Models import Model

models = Model()

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
    

def kmeansModel(document):
    option = input('Execute silhouette test, elbow test or none? (S,E,N)')
    inputData = models.tfidV(data=document)
    if option == 'S':
        clusters = models.silhoutteMeasure(rangeTest=100,data=inputData)
    elif option == 'E':
        clusters = models.elbowMeasure(inputData)
    else:
        clusters = None
    
    gp1 = GraphGen()
    if clusters:
        gp1.lineGraphSingle(titleX="Number of Clusters", titleY="Error "+inputData, rangeX=range(2,100), rangeY=inputData, fig=100)
    inputDoc = models.tfidV(document)    
    kmeans = models.kmeans(data=inputDoc, clusterN=4)
    gp1.spreadGraph(kmeans.cluster_centers_, models.pca2d)
    gp1.showResults()

def bowModel(data):
    result = models.tfidV(data).sum()
    dfsetf = pd.DataFrame({'apperances':result.values, 'word':result.index})
    arrayWordTF = dfsetf.iloc[:,1:].values
    arrayApTF = dfsetf.iloc[:,0].values

    gp = GraphGen()

    gp.barGraph(arrayApTF, arrayWordTF, "Count-Vectorizer", figSize=200)
    gp.showResults()



def main():

    ascii_banner = pyfiglet.figlet_format("NLP Driving Rules Processor")
    print("#########################################################")
    print(ascii_banner)
    print("#########################################################")

    parser = argparse.ArgumentParser()
    parser.add_argument('--source', '-s', type=str, help='Name of source file')
    #parser.add_argument('--csv', '-c', type=str, help='Name of file to save')
    parser.add_argument('--model', '-m', type=str, help='type of model to execute')
    args = parser.parse_args()


    document = openFile(args.source)

    if args.model == 'kmeans':
        kmeansModel(document)
    elif args.model == 'bow':
        bowModel(document)


    print(document)
    args = parser.parse_args()

class Result:
    def __init__(self):
        pass

if __name__ == "__main__":
    main()



