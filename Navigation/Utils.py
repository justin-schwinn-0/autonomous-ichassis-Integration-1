import cProfile
import pstats
from NavigationGraph import *

def ProfileFunction(FuncName:str):

    binFilename = "Profiling/"+FuncName+"_output.dat"
    f = open(binFilename,"w")
    f.write("")
    cProfile.run(FuncName, binFilename)

if __name__ == "__main__":
    ProfileFunction("baseTestCase()")