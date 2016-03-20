import spaceinvaders
import pygame


screen = spaceinvaders.SCREEN
totalWidth=800 #TODO: get this from screen
totalHeight=600 #TODO: get this from screen
debugRectWidth=1
debugRectHeight=5
global shouldDraw
shouldDraw = False
global totalLastTimeUpdated
totalLastTimeUpdated=0
def increaseTotalLastTimeUpdated():
    global totalLastTimeUpdated
    totalLastTimeUpdated+=1
class InputRect:
    def __init__(self, xpos, ypos):
        global totalLastTimeUpdated
        self.lastTimeUpdated=totalLastTimeUpdated
        self.xpos=xpos
        self.ypos=ypos
        self.friendOrFoe=1
        self.width=debugRectWidth
        self.height=debugRectHeight
    def draw(self, surface):
        global totalLastTimeUpdated
        if (self.friendOrFoe==0 or self.lastTimeUpdated<totalLastTimeUpdated):
            return
        if(self.friendOrFoe==1):
            color=spaceinvaders.GREEN
        if(self.friendOrFoe==-1):
            color=spaceinvaders.RED
        pygame.draw.rect(surface,color,(self.xpos,self.ypos,self.width,self.height))
inputRects = []
for i in range(0,totalWidth-debugRectWidth,debugRectWidth):
    inputRects.append([])
    for j in range(0,totalHeight-debugRectHeight,debugRectHeight):
        inputRects[i].append(InputRect(i,j))
def updateRects(arrayToUse, timeToUpdate,valueToUse):
    for element in arrayToUse:
        elementX = element.rect.x
        elementY = element.rect.y
        elementWidth = element.rect.width
        elementHeight = element.rect.height
        for i in range(elementX/debugRectWidth,(elementX + elementWidth)/debugRectWidth):
            for j in range(elementY/debugRectHeight,(elementY + elementHeight)/debugRectHeight):
                if (len(inputRects)<=i or len(inputRects[i])<=j):
                    continue
                inputRects[i][j].friendOrFoe=valueToUse
                inputRects[i][j].lastTimeUpdated=timeToUpdate
modelInputs=[]
def debug(game):
    global modelInputs
    modelInputs=[]
    global totalLastTimeUpdated
    increaseTotalLastTimeUpdated()
    updateRects(game.enemies,totalLastTimeUpdated,-1)
    updateRects(game.enemyBullets,totalLastTimeUpdated,-1)
    updateRects(game.bullets,totalLastTimeUpdated,1)
    updateRects([game.player],totalLastTimeUpdated,1)
    updateRects([game.mysteryShip],totalLastTimeUpdated,-1)
    global shouldDraw
    for rectList in inputRects:
        #rect.decideFriendOrFoe(game)
        for rect in rectList:
            if (shouldDraw):
                rect.draw(game.screen)
            if (rect.lastTimeUpdated==totalLastTimeUpdated):
                modelInputs.append(rect.friendOrFoe)
            else:
                modelInputs.append(0)
if __name__ == '__main__':
    spaceinvaders.main(debug)


