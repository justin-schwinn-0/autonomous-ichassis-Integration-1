from NavAtomicClasses import Node,Path
class NavGraph:
    def __init__(self) -> None:
        self.Nodes = []
        self.Paths = []
        pass

    def setNodes(self, nodes):
        self.Nodes = nodes
        pass

    def AddPaths(self, A:int,B):
        for e in B:
            self.Paths.append()
            pass
        pass
    pass

if __name__ == "__main__":
    nodes =[]

    for i in range(5):
        nodes.append(Node("x",i+0.1,i+0.5,str(i)))

    graph = NavGraph()

    graph.setNodes(nodes)

    graph.AddPaths(1,(2,3,4,5))
    graph.AddPaths(2,(1,3,4))
    graph.AddPaths(3,())

    

    pass    