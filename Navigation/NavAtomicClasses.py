class Node:
    def __init__(self,type:str, X:float, Y:float,label:str)-> None:
        self.type = type
        self.X = X
        self.Y = Y
        self.label = label
        self.connections = []

    def addConnection(self, index):
        if(index not in self.connections):
            self.connections.append(index)
        
    def ConnectionsList(self):
        return self.connections

        #STR format is type(char) | float x | float y | name \n
    def toStr(self) -> str:
        return  self.type +"|"+ str(self.X) +"|"+ str(self.Y) +"|"+ self.label
 

def FromStr(line:str):
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