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
        distances = PathingData(self.Nodes)
        distances.getFullDistances(StartingFrom=B)
        currentDist = distances[A]
        e = A

        path = [A]

        while e != B:
            connected = self.nodes[e].ConnectionsList()
            for i in connected:
                if(distances[i] == currentDist-1):
                    e = i
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
        min_ConnectedDist = min(self.Distances[self.Nodes[index].ConnectionsList()])
        self.Distances[index] = min_ConnectedDist + 1
        self.EnqueueVisits(index)

    def getFullDistances(self,StartingFrom:int):
        self.StartAt(StartingFrom)

        while self.length+1 in self.Distances:
            self.DoVisit()
        
        return self.Distances
        


if __name__ == "__main__":
    nodes =[Node("x",0.1,0.5,str(-1))]

    for i in range(11):
        nodes.append(Node("x",i+0.1,i+0.5,str(i)))

    graph = NavGraph()

    graph.setNodes(nodes)

    graph.AddPaths(1,[2,5])
    graph.AddPaths(2,[1,3,4])
    graph.AddPaths(3,[2,9])
    graph.AddPaths(4,[2,6,8])
    graph.AddPaths(5,[1,6])
    graph.AddPaths(6,[4,7,5])
    graph.AddPaths(7,[6,8])
    graph.AddPaths(8,[4,7,9,10])
    graph.AddPaths(9,[3,8])
    graph.AddPaths(10,[8,11])
    graph.AddPaths(11,[10]) 

    print(graph.PathFromAtoB(1,11))  

    pass    