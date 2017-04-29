from pygame.constants import *
import spaceinvaders
import pygame
import numpy as np
import neuralNetwork as nn
from spaceinvaders import Text

class EventMock:
    def __init__(self):
        self.type = ""
class InputRect:
    def __init__(self, xpos, ypos, mainObject):
        self.lastTimeUpdated=mainObject.totalLastTimeUpdated
        self.xpos=xpos
        self.ypos=ypos
        self.friendOrFoe=1
        self.width= mainObject.debugRectWidth
        self.height= mainObject.debugRectHeight
    def draw(self, surface, totalLastTimeUpdated):
        if (self.friendOrFoe==0 or self.lastTimeUpdated<totalLastTimeUpdated):
            return
        if(self.friendOrFoe==1):
            color=spaceinvaders.GREEN
        if(self.friendOrFoe==-1):
            color=spaceinvaders.RED
        pygame.draw.rect(surface,color,(self.xpos,self.ypos,self.width,self.height))
class SpaceInvadersOverride(spaceinvaders.SpaceInvaders):
    def __init__(self):
        super(SpaceInvadersOverride,self).__init__()
        self.screen = spaceinvaders.SCREEN
        self.totalWidth=800 #TODO: get this from screen
        self.totalHeight=600 #TODO: get this from screen
        self.debugRectWidth=20
        self.debugRectHeight=20
        self.shouldDraw = False
        self.totalLastTimeUpdated=0
        self.fitness = 0
        self.inputRects = []
        for i in range(0,self.totalWidth-self.debugRectWidth,self.debugRectWidth):
            self.inputRects.append([])
            for j in range(0,self.totalHeight-self.debugRectHeight,self.debugRectHeight):
                self.inputRects[i/self.debugRectWidth].append(InputRect(i,j,self))
        self.modelInputs=np.zeros((self.totalWidth/self.debugRectWidth)*(self.totalHeight/self.debugRectHeight))
        self.network = nn.NeuralNetwork(np.array([[600*800/(self.debugRectHeight*self.debugRectWidth),100],[100,10],[10,2]]))
        #self.network = nn.NeuralNetwork(np.array([[600*800/5,2]]))
        self.debugKeys={
            K_LEFT:False,
            K_RIGHT:False,
            K_SPACE:False
        }
        self.o = EventMock()
        self.events = [self.o]
    def increaseTotalLastTimeUpdated(self):
        self.totalLastTimeUpdated+=1

    def updateRects(self,arrayToUse,valueToUse):
        for element in arrayToUse:
            elementX = element.rect.x
            elementY = element.rect.y
            elementWidth = element.rect.width
            elementHeight = element.rect.height
            for i in range(elementX/self.debugRectWidth,(elementX + elementWidth)/self.debugRectWidth):
                for j in range(elementY/self.debugRectHeight,(elementY + elementHeight)/self.debugRectHeight):
                    if (len(self.inputRects)<=i or len(self.inputRects[i])<=j):
                        continue
                    self.inputRects[i][j].friendOrFoe=valueToUse
                    self.inputRects[i][j].lastTimeUpdated=self.totalLastTimeUpdated
    def debug(self,game):
        if(game.mainScreen or game.gameOver):
            print("the score:{0} and the fitness: {1}".format(game.score,self.fitness))
            self.network.setFitness(self.fitness)
            self.fitness = 0
            self.network.createRandomTemp()
            game.reset(0,3)
            game.startGame=True
            game.gameOver=False
            game.mainScreen=False
            return
        self.increaseTotalLastTimeUpdated()
        self.updateRects(game.enemies,-1)
        self.updateRects(game.enemyBullets,-1)
        self.updateRects(game.bullets,1)
        self.updateRects([game.player],1)
        self.updateRects([game.mysteryShip],-1)
        for rectList in self.inputRects:
        #rect.decideFriendOrFoe(game)
            for rect in rectList:
                if (self.shouldDraw):
                    rect.draw(game.screen,self.totalLastTimeUpdated)
                valToInsert=0
                if (rect.lastTimeUpdated==self.totalLastTimeUpdated):
                    valToInsert = rect.friendOrFoe
                self.modelInputs[(rect.ypos/self.debugRectHeight)*(self.totalWidth/self.debugRectWidth)+(rect.xpos/self.debugRectWidth)]=valToInsert
        # print sum(self.modelInputs)
        prediction=self.network.predict(self.modelInputs)
        # print prediction
    #keys[K_LEFT]
        # print prediction
        if(prediction[0]>0.5):
            self.debugKeys[K_RIGHT]=True
            self.debugKeys[K_LEFT]=False
        else:
            self.debugKeys[K_RIGHT]=False
            self.debugKeys[K_LEFT]=True
        if(prediction[1]>0.5):
        # print "Want to fire"
            self.debugKeys[K_SPACE]=True
        else:
            self.debugKeys[K_SPACE]=False
        self.updateScore(game)

    def updateScore(self,game):
        self.fitness += game.score
    def getKeys(self):
        # print "other get keys"
        # print self.debugKeys
        return self.debugKeys
    def main(self):
        super(SpaceInvadersOverride,self).main((lambda game: self.debug(game)))

    def getEvents(self):
        curEvents = super(SpaceInvadersOverride,self).getEvents()
        if len(curEvents)>0: return curEvents
        return self.events
if __name__ == '__main__':
    spaceinvaders.game=SpaceInvadersOverride()
    spaceinvaders.timeMultiplier=1
    spaceinvaders.main()


