from NavigationGraph import NavGraph
from NavAtomicClasses import Node
import math


def AngleFromAToB(a,b)-> float:
    ax,ay = a.getLocation()
    bx,by = b.getLocation()

    radians = math.atan2(by-ay,bx-ax)
    angle = math.degrees(radians)

    return angle

def AngleFromAtoXY(a,X,Y)->float:
    ax,ay = a.getLocation()
    bx,by = X,Y

    radians = math.atan2(by-ay,bx-ax)
    angle = math.degrees(radians)

    return angle

def distanceFromAtoB(a,b)-> float:
    ax,ay = a.getLocation()
    bx,by = b.getLocation()
    return math.sqrt((bx-ax)**2 + (by-ay)**2)

#turns a -180-180 into 0-360 angle
def fixAngle(angle): 
    if angle < 0:
        angle += 360
    return angle % 360

def fixAngle180(angle):
    newAngle = angle
    if(newAngle > 360):
        newAngle = newAngle % 360
    elif(newAngle > 180):
        newAngle -= 360
    elif(newAngle <= -180):
        newAngle = -(-newAngle % -180)
        
    return newAngle
class Car:
    
    AngleTolerance = 10.0
    NodeDistanceTolerance = 0.05
    MaxTurn = 30                    # for testing purposes, not used on piccar
    TurningMoveSpeed = 0.1
    NormalSpeed = .4

    def __init__(self) -> None:
        self.angle = 0.0
        self.X = 0
        self.Y = 0 
    
    # returns the direction of the car and the difference between the direction of the car and the desired direction of the car to hit the next node
    def getturnData(self, targetAngle): #L is left, x is no turn, R is right
        angleDiff = self.angle - targetAngle

        absDiff = abs(angleDiff)
        dir = 0
        # L is left, x is no turn, R is right
        if(absDiff < Car.AngleTolerance):
            dir = "x"
        elif(angleDiff <= 180): # turn left
            dir = 'L'
        else:
            dir = 'R'

        return dir,angleDiff


    def getTurnDataPICAR(self, tX,tY): # takes in targetX and target y coords
        target_Angle = AngleFromAtoXY(self,tX,tY)

        angleDifferential = fixAngle180(target_Angle - self.angle)
        dir = 'x'

        if(angleDifferential > 180):
            angleDifferential = 360- angleDifferential

        if(abs(angleDifferential) < Car.AngleTolerance):
            dir = 'x'
        elif(angleDifferential > 0): #turn left
            dir = 'L'
        else:
            dir = 'R'
        
        return dir, angleDifferential
    #turning logic and simulation, not for picar, might be resused later if we need a microsim
    def turn(self,direction, angleDelta): # most of this code would be repleaced by calls to PicarTurnleft
        if(direction == 'x'):
            return None
        
        coef = -1 if direction == 'L' else 1
        turnAmount = min(abs(angleDelta),Car.MaxTurn)

        self.angle += coef * turnAmount
        self.angle = fixAngle(self.angle)

    #simulation, not for picar
    def move(self,direction):
        carSpeed = Car.NormalSpeed if direction == 'x' else Car.TurningMoveSpeed
        radAngle = math.radians(self.angle)
        self.X += carSpeed * math.cos(radAngle)
        self.Y += carSpeed * math.sin(radAngle)

    def getLocation(self):
        return self.X,self.Y

    def setLocation(self,x:float,y:float):
        self.X = x
        self.Y = y

    def setAngle(self, newAngle):
        self.angle = fixAngle180(newAngle)

    def __str__(self) -> str:
        return f"X:{self.X:2.4f} Y:{self.Y:2.4f} A:{self.angle:3.4f}"

def Test1Nodes():
    a = Node('x',-2,0,"A")
    b = Node('x',1,0,"B")
    c = Node('x',3,2,"C")
    d = Node('x',5,0,"D")
    e = Node('x',6,0.1,"D")
    f = Node('x',7,0,"D")

    return [a,b,c,d,e,f]

def Test2Nodes():
    a = Node('x',0,0,"A")
    b = Node('x',1,0,"B")
    c = Node('x',2,-0.5,"C")
    d = Node('x',1,-1,"D")
    e = Node('x',-1,1,"D")
    f = Node('x',-2,0,"D")

    return [a,b,c,d,e,f]

def Test3Nodes():
    a = Node('x',0,0,"A")
    b = Node('x',0.5,-0.5,"B")
    c = Node('x',2,-0.5,"C")
    d = Node('x',0,0,"D")
    e = Node('x',-1,1,"D")
    f = Node('x',-2,0,"D")

    return [a,b,c,d,e,f]

def test4Nodes():
    a = Node('x',0,0,"A")
    b = Node('x',3,2,"B")
    c = Node('x',3,0,"C")
    d = Node('x',3,1,"D")
    e = Node('x',6,2,"E")
    f = Node('x',6,0,"F")
    g = Node('x',5.5,1,"G")

    return [a,b,c,d,e,f,g]

    pass
#keep
def TestCase1():

    # might need to trim these numbers, 
    # 6 or 7 digits of percision is should be good, 
    # if we even have that much percision in the GPS

    graph = NavGraph()
    graph.setNodes(Test1Nodes())

    graph.AddPaths(0,[1])
    graph.AddPaths(1,[2])
    graph.AddPaths(2,[3])
    graph.AddPaths(3,[4])
    graph.AddPaths(4,[5])

    path = graph.PathFromAtoB(0,5)

    return path,graph

def MoveTestCase(index:int = 3):
    graph = NavGraph()
    graph.setNodes(Test2Nodes())

    graph.AddPaths(0,[1])
    graph.AddPaths(1,[2])
    graph.AddPaths(2,[3])
    graph.AddPaths(3,[4])
    graph.AddPaths(4,[5])


    path = graph.PathFromAtoB(0,index)

    print("gets done with move test case")
    return path,graph

def DemoCase(index:int = 3):
    graph = NavGraph()
    graph.setNodes(test4Nodes())

    graph.AddPaths(0,[1])
    graph.AddPaths(1,[2])
    graph.AddPaths(2,[3])
    graph.AddPaths(3,[4])
    graph.AddPaths(4,[5])
    graph.AddPaths(5,[6])


    path = graph.PathFromAtoB(0,index)

    print("gets done with move test case")

    return path,graph


def turnTestCase(index:int = 3):
    graph = NavGraph()
    graph.setNodes(Test3Nodes())

    graph.AddPaths(0,[1])
    graph.AddPaths(1,[2])
    graph.AddPaths(2,[3])
    graph.AddPaths(3,[4])
    graph.AddPaths(4,[5])

    path = graph.PathFromAtoB(0,index)

    return path,graph


#just testing angles, ignore
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


#don't use this at all
def Traverse1(path,graph:NavGraph):
    
    for i in range(len(path)-1):
        a= graph.Nodes[i]
        b= graph.Nodes[i+1]
        angleAB =AngleFromAToB(a,b)
        direction, angleDiff = c.getturnData(angleAB)
        print("Target angle:",angleAB,direction,angleDiff)
    pass

#this function should not be used on the picar
def TraverseToNode(graph:NavGraph,targetIndex:int,c:Car)->bool: 
    # return true if reached node, false otherwise
    
    #if object detection is good, go on
    #if path finding is good, go on.

    targetAngle = AngleFromAToB(c,graph.Nodes[targetIndex])
    distanceToTarget = distanceFromAtoB(c,graph.Nodes[targetIndex])
    if distanceToTarget < Car.NodeDistanceTolerance: # reached node, return true
        return True
    else: 
        #turn the car if necessary
        # then move forward at a low speed if turning, higher if no turn
        direction, angleDelta = c.getturnData(targetAngle)
        c.turn(direction, angleDelta)
        c.move(direction)

        targetlocX, targetlocY = graph.Nodes[targetIndex].getLocation()
        carLocX, carLocY = c.getLocation()
        print(f"target: ({targetlocX:3.4f},{targetlocY:3.4f}) Car Location: ({carLocX:3.4f},{carLocY:3.4f}) Car angle: {c.angle:3.4f} angle Delta: {angleDelta:3.4f}")

    return False

def TraverseToNodePICAR(graph:NavGraph,targetIndex:int,c:Car)->bool: 
    # return true if reached node, false otherwise
    
    #if object detection is good, go on
    #if path finding is good, go on.

    distanceToTarget = distanceFromAtoB(c,graph.Nodes[targetIndex])
    if distanceToTarget < Car.NodeDistanceTolerance: # reached node, return true
        return True,None,None
    else: 
        # turn the car if necessary
        # then move forward at a low speed if turning, higher if no turn
        nodeX,nodeY = graph.Nodes[targetIndex].getLocation()
        direction, angleDelta = c.getTurnDataPICAR(nodeX,nodeY)
        # targetlocX, targetlocY = graph.Nodes[targetIndex].getLocation()
        # carLocX, carLocY = c.getLocation()
        #print(f"target: ({targetlocX:3.4f},{targetlocY:3.4f}) Car Location: ({carLocX:3.4f},{carLocY:3.4f}) Car angle: {c.angle:3.4f} angle Delta: {angleDelta:3.4f}")

    return False,direction, angleDelta


# python3 traversal.py starts here
if __name__ == "__main__":
    p,g = TestCase1()
    c = Car()
    

    for a in range(-360,400,15):
        print(f"{a} to {math.sin(math.radians(a))}")


    i = 0
    while i < len(p):
        # p[] = path of nodes in order to reach the destination
        reachedTargetNode = TraverseToNode(g,p[i],c)
        if(reachedTargetNode):
            print("node",i, "reached")
            print(f"dist: {distanceFromAtoB(c,g.Nodes[p[i]])}")
            i+=1
    print("destination reached")
