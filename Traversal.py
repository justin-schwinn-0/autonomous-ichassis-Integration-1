import os,sys
sys.path.append("./Navigation")

from NavigationGraph import NavGraph
from NavAtomicClasses import *
import math

def AngleFromAToB(a,b)-> float :
    ax,ay = a.getLocation()
    bx,by = b.getLocation()

    radians = math.atan2(by-ay,bx-ax)
    angle = math.degrees(radians)

    return angle

def distanceFromAtoB(a,b)-> float:
    ax,ay = a.getLocation()
    bx,by = b.getLocation()
    return math.sqrt((bx-ax)**2 + (by-ay)**2)

def fixAngle(angleDiff):
    remainder = angleDiff % 180
    newAngle = angleDiff
    if(angleDiff > 180 or angleDiff < -180):
        newAngle = remainder
        
    return newAngle

class Car:
    
    AngleTolerance = 5.0
    NodeDistanceTolerance = 0.2
    MaxTurn = 30                    # for testing purposes, not used later
    TurningMoveSpeed = 0.2
    NormalSpeed = .4

    def __init__(self) -> None:
        self.angle = 0.0
        self.X = 0
        self.Y = 0 
        #temp class, will be replaced by actual piCar class later.
        #this allows testing simulations
    
    def getturnData(self, targetAngle): #L is left, x is no turn, R is right
        angleDiff = targetAngle - self.angle

        angleDiff = fixAngle(angleDiff)

        absDiff = abs(angleDiff)
        dir = 0

        if(absDiff < Car.AngleTolerance):
            dir = "x"
        elif(angleDiff <= 0): # turn left
            dir = 'L'
        else:
            dir = 'R'

        return dir,angleDiff


    def turn(self,direction, angleDelta): # most of this code would be repleaced by calls to PicarTurnleft
        if(direction == 'x'):
            return None
        
        coef = -1 if direction == 'L' else 1
        turnAmount = min(abs(angleDelta),Car.MaxTurn)

        self.angle += coef * turnAmount
        self.angle = fixAngle(self.angle)

    def move(self,direction):
        carSpeed = Car.NormalSpeed if direction == 'x' else Car.TurningMoveSpeed
        radAngle = math.radians(self.angle)
        self.X += carSpeed * math.cos(radAngle)
        self.Y += carSpeed * math.sin(radAngle)

    def getLocation(self):
        return self.X,self.Y
    
def testCase():
    #            C
    #           / \        
    #    A -- B     D--e--f
    a = Node('x',-2,0,"A")
    b = Node('x',1,0,"B")
    c = Node('x',2,1,"C")
    d = Node('x',3,0,"D")
    e = Node('x',4,.1,"E")
    f = Node('x',6,.2,"E")

    graph = NavGraph()
    graph.setNodes([a,b,c,d,e,f])

    graph.AddPaths(0,[1])
    graph.AddPaths(1,[2])
    graph.AddPaths(2,[3])
    graph.AddPaths(3,[4])
    graph.AddPaths(4,[5])

    path = graph.PathFromAtoB(0,5)

    return path,graph

def TestAngles():
    a = Node('x',0,0,"A")
    b = Node('x',1,1,"B") #45
    c = Node('x',-1,1,"C") # 135
    d = Node('x',1,-1 ,"D") #-45
    e = Node('x',-1,-1 ,"D") #-135
    f = Node('x',-1,0 ,"D") #-180/180

    bangle = AngleFromAToB(a,b)
    cangle = AngleFromAToB(a,c)
    dangle = AngleFromAToB(a,d)
    eangle = AngleFromAToB(a,e)
    fangle = AngleFromAToB(a,f)

    print(bangle)
    print(cangle)
    print(dangle)
    print(eangle)
    print(fangle)

def Traverse1(path,graph:NavGraph):
    
    for i in range(len(path)-1):
        a= graph.Nodes[i]
        b= graph.Nodes[i+1]
        angleAB =AngleFromAToB(a,b)
        direction, angleDiff = c.getturnData(angleAB)
        print("Target angle:",angleAB,direction,angleDiff)
    pass

def TraverseToNode(graph:NavGraph,targetIndex:int,c:Car)->bool: # return true if reached node, false otherwise
    #if object detection is good, go on
    #if path finding is good, go on.
    targetAngle = AngleFromAToB(c,graph.Nodes[targetIndex])
    distanceToTarget = distanceFromAtoB(c,graph.Nodes[targetIndex])
    if distanceToTarget < Car.NodeDistanceTolerance: # reached node, return true
        return True
    else: #turn the car if necessary, then move forward at a low speed if turning, higher if no turn
        direction, angleDelta = c.getturnData(targetAngle)
        c.turn(direction, angleDelta)
        c.move(direction)

        print(f"target: {graph.Nodes[targetIndex].getLocation()} Car Location: {c.getLocation()} Car angle: {c.angle} angle Delta: {angleDelta}")

    return False
    



if __name__ == "__main__":
    p,g =testCase()
    c = Car()
    #Traverse1(p,g)
    #TestAngles()

    print(-185%180)

    i = 0
    while i < len(p):
        reachedTargetNode = TraverseToNode(g,p[i],c)
        if(reachedTargetNode):
            print("node",i, "reached")
            i+=1
    print("destination reached")