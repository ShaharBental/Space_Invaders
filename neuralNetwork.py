import numpy as np
def sigmoid(x):
        return 1/(1+np.exp(-x))
class NeuralNetwork:
    def __init__(self,dimensions):
        self.layers=[]
        self.dims=dimensions
        for i in range(0,dimensions.shape[0]):
            currentLayer = np.random.random((dimensions[i,0],dimensions[i,1]))-1 #mean to 0
            self.layers.append(currentLayer)
        self.tempCoefficients=None
        self.fitness=0
    def createRandomTemp(self):
        tempCoefficients=[]
        for i in range(0,self.dims.shape[0]):
            currentLayer = (np.random.random((self.dims[i,0],self.dims[i,1]))-1)/10 #mean to 0
            tempCoefficients.append(currentLayer + self.getCoefficientsVector(i))
        self.tempCoefficients=self.layers
        self.layers=tempCoefficients
    def setFitness(self,fitness):
        if (fitness>self.fitness):
            self.fitness=fitness
        elif (not self.tempCoefficients is None): self.layers=self.tempCoefficients
        self.tempCoefficients=None
    def getCoefficientsVector(self,layer):
        coeffs=[]
        arr = np.array(self.layers[layer][:,:])
        for j in range(0,arr.__len__()):
            coeffs.append(arr[j])
        return coeffs
    def setCoefficientsVector(self,newVec):
        ammountOfVars = self.dims[:,0]*self.dims[:,1]
        latestPos=0
        for i in range(0,self.layers.__len__()):
            for j in range(0,self.layers[i].shape()[0]):
                for k in range(0,self.layers[i].shape()[1]):
                    self.layers[i][j,k]=newVec[latestPos]
                    latestPos +=1
    def predict(self,inputVec):
        curInput = inputVec
        for i in range(0,self.layers.__len__()):
            curInput= sigmoid(np.dot(curInput,self.layers[i]))
        return curInput

