import matplotlib.pyplot as plt

class GraphGen:
    def __init__(self, data, names):
        self.data = data
        self.names = names
    def barGraph(self):
        fig = plt.figure(figsize=(10,7))
        for i in range(0,len(self.data)):
            plt.bar(self.names[i], self.data[i], label="$"+self.names[i]+"$", width=0.3 )
       
        plt.legend()
        #plt.xlabel('Sampling type', fontsize=14)
        plt.xlabel('$Samplers$', fontsize=14)
        
        plt.title("$Successfull$ $Attacks$")
        plt.show()
