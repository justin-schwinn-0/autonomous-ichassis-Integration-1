import struct

class Node:
    def __init__(self,type:str, X:int, Y:int,label:str)-> None:
        self.type = type
        self.X = X
        self.Y = Y
        self.label = label
        pass

        #STR format is 8b_Type (Char) | 32b_X_Loc | 32b_Y_Loc | N-Byte label \n
    def FromLine(line:str):
        [t,x,y,l] = struct.unpack('cii4s',line.encode())
        n = Node(t,x,y,l)
        return n

    def toByteString(self):
        return struct.pack('cffp',self.type,self.X,self.Y,self.label)
    
class Path:
    def __init__(self,A:Node,B:Node) -> None:
        self.A = A
        self.B = B
        pass

if __name__ == "__main__":
    t = 'c'
    x = 0.4
    y = 0.6
    l = "name"
    node = Node(t,x,y,l)

    L = "c00000000name"

    line = struct.unpack("cii4s",L.encode())

    n2 = Node.FromLine(line)

    test = n2.toByteString().decode()

    pass