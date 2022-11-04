import matplotlib.pyplot as plt

class GraphGen:
    def __init__(self):
       pass
    def barGraph(self, data, names):
        fig = plt.figure(figsize=(10,7))
        for i in range(0,len(data)):
            plt.bar(names[i], data[i], label="$"+names[i]+"$", width=0.3 )
       
        plt.legend()
        #plt.xlabel('Sampling type', fontsize=14)
        plt.xlabel('$Samplers$', fontsize=14)
        
        plt.title("$Successfull$ $Attacks$")
    def showResults(self):
        plt.show()

    
