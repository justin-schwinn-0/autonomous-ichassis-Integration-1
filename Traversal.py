from Navigation.NavigationGraph import *
from Navigation.NavAtomicClasses import Node
import math

def AngleFromAToB(a:Node,b:Node)-> float :
    ax,ay = a.getLocation()
    bx,by = b.getLocation()

    radians = math.atan2(by-ay,bx-ax)
    angle = math.degrees(radians)

    return angle


class Car:
    def __init__(self) -> None:
        self.angle = 0.0
        #temp class, will be replaced by actual piCar class later.
        # this allows testing simulations
        pass


def testCase():
    #           C
    #          / \
    #    A - B     D
    a = Node('x',0,0,"A")
    b = Node('x',1,0,"A")
    c = Node('x',2,1,"A")
    d = Node('x',3,0,"A")

    graph = NavGraph()
    graph.setNodes([a,b,c,d])

    graph.AddPaths(0,1)
    graph.AddPaths(1,2)
    graph.AddPaths(2,3)

    path = graph.PathFromAtoB(0,3)

    print(path)

def Traverse():

    pass


if __name__ == "__main__":
    testCase()