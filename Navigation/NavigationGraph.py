from NavAtomicClasses import Node
class NavGraph:
    def __init__(self) -> None:
        self.Nodes = []
        pass

    def setNodes(self, nodes):
        self.Nodes = nodes
        pass

    def AddPaths(self, A:int,B):
        for e in B:
            self.Nodes[A].addConnection(e)
            self.Nodes[e].addConnection(A)
        pass

    def PathFromAtoB(self, A ,B):
        distances = PathingData(self.Nodes).getFullDistances(StartingFrom=B)
        currentDist = distances[A]
        e = A

        path = [A]

        while e != B:
            connected = self.Nodes[e].ConnectionsList()
            for i in connected:
                if(distances[i] == currentDist-1):
                    e = i
                    currentDist -=1
                    path.append(e)
        return path
        

class PathingData:

    def __init__(self,nodes) -> None:
        self.Visited = []
        self.Distances = []
        self.nodeQueue = []
        self.Nodes = nodes
        self.length = len(nodes)

        for i in range(self.length):
            self.Distances.append(self.length+1)
            self.Visited.append(False)

    def StartAt(self, end:int):
        self.Visited[end] = True
        self.Distances[end] = 0
        self.EnqueueVisits(self.Nodes[end].ConnectionsList())

    
    def EnqueueVisits(self, ps):
        for p in ps:
            if(not self.Visited[p]):
                self.Visited[p] = True
                self.nodeQueue.append(p)
    
    def DoVisit(self):
        index = self.nodeQueue.pop(0)
        distToCheck = []
        for i in self.Nodes[index].ConnectionsList():
            distToCheck.append(self.Distances[i])
        min_ConnectedDist = min(distToCheck)
        self.Distances[index] = min_ConnectedDist + 1
        self.EnqueueVisits(self.Nodes[index].ConnectionsList())

    def getFullDistances(self,StartingFrom:int):
        self.StartAt(StartingFrom)

        while self.length+1 in self.Distances:
            self.DoVisit()
        
        return self.Distances
        


if __name__ == "__main__":
    nodes =[]

    for i in range(11):
        nodes.append(Node("x",i+0.1,i+0.5,str(i)))

    graph = NavGraph()

    graph.setNodes(nodes)

    graph.AddPaths(0,[1,4])
    graph.AddPaths(1,[0,2,3])
    graph.AddPaths(2,[1,8])
    graph.AddPaths(3,[1,5,7])
    graph.AddPaths(4,[0,5])
    graph.AddPaths(5,[3,6,4])
    graph.AddPaths(6,[5,7])
    graph.AddPaths(7,[3,6,8,9])
    graph.AddPaths(8,[2,7])
    graph.AddPaths(9,[7,10])
    graph.AddPaths(10,[9]) 

    print(graph.PathFromAtoB(0,10))  

    pass    