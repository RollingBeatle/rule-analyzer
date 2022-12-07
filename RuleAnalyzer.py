import argparse
import logging
import os
from pydoc import doc
import pyfiglet
import pandas as pd
from tools.GraphGen import GraphGen
import pandas as pd
from models.Models import Model
import seaborn as sns

models = Model()

def openFile(filename):
    lines = []
    with open("./data/"+filename) as file:
        lines = [line.rstrip('\n') for line in file]
    return lines

def export(frame, name):
    frame.to_csv('./results/'+name+'.csv')


def kmeansModel(document):
    option = input('Execute silhouette test, elbow test or none? (S,E,N)')
    inputData = models.tfidV(data=document)
    if option == 'S':
        clusters = models.silhoutteMeasure(rangeTest=100,data=inputData)
    elif option == 'E':
        clusters = models.elbowMeasure(rangeTest=100, data=inputData)
    else:
        clusters = None
    clusterNumb = input('Please input the number of cluster to work with: \n')
    gp1 = GraphGen()
    if clusters:
        gp1.lineGraphSingle(titleX="Number of Clusters", titleY="Error "+inputData, rangeX=range(2,100), rangeY=inputData, fig=100)
    inputDoc = models.tfidV(document)    
    kmeans = models.kmeans(data=inputDoc, clusterN=int(clusterNumb))
    df = pd.DataFrame()

    cluster_map ={}
    for i in range (0,int(clusterNumb)):
        cluster_map.update({i: "Cluster "+str(i+1)})

    df['cluster'] = models.labels
    df['cluster'] = df['cluster'].map(cluster_map)
    df['x0'] = models.x0
    df['x1'] = models.x1
    gp1.scatterSNS(df)
    #gp1.spreadGraph(kmeans.cluster_centers_, models.pca2d)  ,  3: "Cluster 4", 4: "Cluster 5"
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


    #print(document)
    args = parser.parse_args()

class Result:
    def __init__(self):
        pass

if __name__ == "__main__":
    main()



