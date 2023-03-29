class Node:

    # The constructor, each node has an x and y value. x and y are the longitude and latitude respectively. connections denote the neighbors to a node.
    def __init__(self,type:str = 'x', X:float=0, Y:float=0,label:str="")-> None:
        self.type = type
        self.X = X
        self.Y = Y
        self.label = label
        self.connections = []
    
    # addConnection() is used to add a neighbor to the node.
    def addConnection(self, index):
        if(index not in self.connections):
            self.connections.append(index)
        return self
   
    # uses addConnection() alot
    def addManyConnections(self, list):
        for i in list:
            self.addConnection(i)
        return self
        
    def ConnectionsList(self):
        return self.connections
    
    def getLocation(self):
        return self.X,self.Y

    # ConnectionListasStr() parses a lin from the input file and assigns the connections denoted in the input file to the self node
    def ConnectionListasStr(self)->str:
        if(len(self.connections) == 0):
            return "ERR"
        
        string = str(self.connections[0])

        for i in self.connections[1:]:
            string += "," + str(i)

        return string

        #STR format is type(char) | float x | float y | name \n
    def toStr(self) -> str:
        return  self.type +"|"+ str(self.X) +"|"+ str(self.Y) +"|"+ self.label
    
    def resetDatawStr(self,data:str):
        [t,x,y,l] = data.split("|")
        self.type = type
        self.X = x
        self.Y = y
        self.label = l
 

def NodeFromStr(line:str):
    [t,x,y,l] = line.split("|")
    n = Node(t,float(x),float(y),l)
    return n
    
if __name__ == "__main__":
    t = 'c'
    x = 0.4
    y = 0.6
    l = "name"
    node = Node(t,x,y,l)

    print(node.toStr())

    pass
