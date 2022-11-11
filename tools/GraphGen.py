import matplotlib.pyplot as plt

class GraphGen:
    def __init__(self):
       pass
    
    def barGraph(self, data, names, title):
        fig = plt.figure(figsize=(10,7))
        for i in range(0,len(data)):
            plt.bar(names[i], data[i],  width=0.3 ) #label="$"+names[i]+"$",

        plt.legend()
        #plt.xlabel('Sampling type', fontsize=14)
        plt.xlabel('$Words$', fontsize=14)
        plt.xticks([])
        plt.title("$"+title+"$")

    def showResults(self):
        plt.show()

    def lineGraphSingle (self, rangeX, rangeY, titleX, titleY):
        plt.plot(rangeX, rangeY)
        plt.xticks(rangeX)
        plt.xlabel(titleX)
        plt.ylabel(titleY)

    def spreadGraph(self, coordX, coordY):
        plt.scatter(coordY[:,0], coordY[:,1])
        plt.scatter(coordX[:,0], coordX[:,1], c='black', s=300, alpha=0.6)
        



    
