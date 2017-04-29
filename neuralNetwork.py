import os.path

import numpy as np
def sigmoid(x):
        return 1/(1+np.exp(-x))
class NeuralNetwork:
    def __init__(self,dimensions):
        self.fileName = "neuralNetwork.dat"
        self.layers=[]
        self.dims=dimensions
        if os.path.isfile(self.fileName + ".npz"):
            self.layers = np.load(self.fileName + ".npz")['arr_0']
        else:
            for i in range(0,dimensions.shape[0]):
                currentLayer = (2*np.random.random((dimensions[i,0],dimensions[i,1]))-1)/100 # mean to 0
                # print currentLayer
                self.layers.append(currentLayer)
        self.tempCoefficients=None
        self.fitness=0
    def createRandomTemp(self):
        tempCoefficients=[]
        for i in range(0,self.dims.shape[0]):
            currentLayer = (2 * (np.random.random((self.dims[i,0],self.dims[i,1]))) - 1)/10 # mean to 0
            tempCoefficients.append(currentLayer + self.getCoefficientsVector(i))
        self.tempCoefficients=self.layers
        self.layers= tempCoefficients
        # print self.layers
    def setFitness(self,fitness):
        if (not self.tempCoefficients is None and (fitness+self.fitness>0)):
            for i in range(0,self.dims.shape[0]):
                self.layers[i] = (self.tempCoefficients[i]*self.fitness + fitness*self.layers[i])*(1/(self.fitness+fitness))
        if (fitness>self.fitness):
            print "new score is better, new score is {0}".format(fitness)
            self.fitness=fitness
            np.savez(self.fileName,self.layers)
        else:
            print "old score is better, staying with max of {0}".format(self.fitness)
            #self.layers=self.tempCoefficients
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
            # print "dot"
            # print np.dot(curInput,self.layers[i])
            curInput= sigmoid(np.dot(curInput,self.layers[i]))
        return curInput

