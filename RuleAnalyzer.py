import argparse
import logging
import os
from pydoc import doc
import pyfiglet
import pandas as pd
from models.WordBag import WordBag
from tools.GraphGen import GraphGen
import pandas as pd

def openFile(filename):
    lines = []
    with open("./data/"+filename) as file:
        lines = [line.rstrip('\n') for line in file]
    return lines
def export(frame, name):
    frame.to_csv('./results/'+name+'.csv')

def compareDataFrameResults(dataSk, dataTf):
    sesumSk = dataSk.sum()

    dfsesumsk=pd.DataFrame({'apperances':sesumSk.values, 'word':sesumSk.index})
    arrayWord = dfsesumsk.iloc[:,1:].values
    arrayAp = dfsesumsk.iloc[:,0].values

    print(arrayAp)
    print(arrayWord)
    GraphGen().barGraph(arrayAp,arrayWord)
    GraphGen().showResults()

    dfsumTf = dataTf.sum()
    print(dfsumTf)


if __name__ == "__main__":
    ascii_banner = pyfiglet.figlet_format("Natural Lang Processor")
    print("#########################################################")
    print(ascii_banner)
    print("#########################################################")
    logging.basicConfig()
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', '-n', type=str, help='Name of data file')
    parser.add_argument('--csv', '-c', type=str, help='Name of file to save')
    
    args = parser.parse_args()

    document = openFile(args.name)
    print(document)

    modelPL = WordBag(document)
    modelPL.tf_ldf(False)
    dfTf = modelPL.res
    modelPL.skImpl()
    dfsk = modelPL.res

    compareDataFrameResults(dfsk,dfTf)

    ##export(modelPL.res, args.csv)


