import matplotlib.pyplot as plt
import seaborn as sns

class GraphGen:
    def __init__(self):
       pass
    
    def barGraph(self, data, names, title, figSize):
        #fig = plt.figure(figsize=(10,7))
        plt.figure(figSize)
        for i in range(0,len(data)):
            plt.bar(names[i], data[i],  width=0.3 ) #label="$"+names[i]+"$",

        plt.legend()
        #plt.xlabel('Sampling type', fontsize=14)
        plt.xlabel('$Words$', fontsize=14)
        plt.xticks([])
        plt.title("$"+title+"$")

    def showResults(self):
        plt.show()

    def lineGraphSingle (self, rangeX, rangeY, titleX, titleY,fig):
        plt.figure(fig)
        plt.plot(rangeX, rangeY)
        plt.xticks(rangeX)
        plt.xlabel(titleX)
        plt.ylabel(titleY)

    def spreadGraph(self, coordX, coordY):
        plt.scatter(coordY[:,0], coordY[:,1])
        plt.scatter(coordX[:,0], coordX[:,1], c='black', s=300, alpha=0.6)

    def scatterSNS(self,dataF):
        plt.figure(figsize=(12, 7))
        # set title
        plt.title("Clustering k-means TF-IDF", fontdict={"fontsize": 18})
        # set axes names
        plt.xlabel("X0", fontdict={"fontsize": 16})
        plt.ylabel("X1", fontdict={"fontsize": 16})
        #  create scatter plot with seaborn, where hue is the class used to group the data
        #for i in dataF:
        print(dataF)
        sns.scatterplot(data=dataF, x='x0', y='x1', hue='cluster')
        
