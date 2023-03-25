class Node:
    def __init__(self,type:str = 'x', X:float=0, Y:float=0,label:str="")-> None:
        self.type = type
        self.X = X
        self.Y = Y
        self.label = label
        self.connections = []

    def addConnection(self, index):
        if(index not in self.connections):
            self.connections.append(index)
        return self
    
    def addManyConnections(self, list):
        for i in list:
            self.addConnection(i)
        return self
        
    def ConnectionsList(self):
        return self.connections
    
    def getLocation(self):
        return self.X,self.Y

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