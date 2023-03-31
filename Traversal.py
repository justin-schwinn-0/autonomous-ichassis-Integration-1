import os,sys
sys.path.append("./Navigation")
sys.path.append("./RPi-Chassis")
#might need to change these if bridgette switched around the folders

from NavigationGraph import NavGraph
from NavAtomicClasses import *
import GPS
import math

piCar = Picarx()

def AngleFromAToB(a,b)-> float:
    ax,ay = a.getLocation()
    bx,by = b.getLocation()

    radians = math.atan2(by-ay,bx-ax)
    angle = math.degrees(radians)

    return angle

def distanceFromAtoB(a,b)-> float:
    ax,ay = a.getLocation()
    bx,by = b.getLocation()
    return math.sqrt((bx-ax)**2 + (by-ay)**2)

#turns a 0 to 360 angle into a -180 to 180 angle
def fixAngle(angleDiff): 
    remainder = angleDiff % 180
    newAngle = angleDiff
    if(angleDiff > 180 or angleDiff < -180):
        newAngle = remainder
        
    return newAngle

class Car:
    
    AngleTolerance = 5.0
    NodeDistanceTolerance = 0.2
    MaxTurn = 30                    # for testing purposes, not used on piccar
    TurningMoveSpeed = 0.2
    NormalSpeed = .4

    def __init__(self) -> None:
        self.angle = 0.0
        self.X = 0
        self.Y = 0 
    
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

    def UpdateLocation(self):
        latitude,longitude = GPS.get_coordinates()

    def UpdateCourse(self):
        course, unused_speed = GPS.get_course_speed()
        self.angle = fixAngle(course)

    def PiCARturn(self, direction):
        if(direction == 'x'):
            return None
        
        if(direction == 'L'):
         piCar.steer_left()
        else:
         piCar.steer_right()

    #always move forward, forward() should slow the car down while turning
    def PiCARMove():
        piCar.forward(Car.NormalSpeed)

#keep
def testCase():

    a = Node('x',32.99328671685252, -96.75160268387103,"A")
    b = Node('x',32.99339582533694, -96.75160536608,"B")
    c = Node('x',32.99340482396881, -96.75150746545252,"C")
    d = Node('x',32.993400324653, -96.75143638691478,"D")

    # might need to trim these numbers, 
    # 6 or 7 digits of percision is should be good, 
    # if we even have that much percision in the GPS

    graph = NavGraph()
    graph.setNodes([a,b,c,d])

    graph.AddPaths(0,[1])
    graph.AddPaths(1,[2])
    graph.AddPaths(2,[3])

    path = graph.PathFromAtoB(0,3)

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

        print(f"target: {graph.Nodes[targetIndex].getLocation()} Car Location: {c.getLocation()} Car angle: {c.angle} angle Delta: {angleDelta}")

    return False
    
# return true if reached node, false otherwise
def TraverseToNodeGPS(graph:NavGraph,targetIndex:int,c:Car)->bool: 
    #if object detection is good, go on
    #if path finding is good, go on.

    c.UpdateCourse()
    c.UpdateLocation()

    targetAngle = AngleFromAToB(c,graph.Nodes[targetIndex])
    distanceToTarget = distanceFromAtoB(c,graph.Nodes[targetIndex])
    if distanceToTarget < Car.NodeDistanceTolerance: # reached node, return true
        return True
    else: 
        # turn the car if necessary 
        # then move forward at a low speed if turning, higher if no turn
        # it looks like "move slow if moving" is built into picar.forward()

        direction, angleDelta = c.getturnData(targetAngle)
        c.PiCARturn(direction)
        c.PiCARMove()

        debugstring = ""
        debugstring += f" target: {graph.Nodes[targetIndex].getLocation()}" 
        debugstring += f" Car Location: {c.getLocation()}"
        debugstring += f" Car angle: {c.angle}"
        debugstring += f" angle Delta: {angleDelta}"

        print(debugstring)
       
    return False



if __name__ == "__main__":
    p,g = testCase()
    c = Car()
    

    i = 0
    while i < len(p):
        reachedTargetNode = TraverseToNode(g,p[i],c)
        if(reachedTargetNode):
            print("node",i, "reached")
            i+=1
    print("destination reached")
    piCar.stop()