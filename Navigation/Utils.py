import cProfile
import pstats

def ProfileFunction(FuncName:str):
    cProfile.run(FuncName+"()","Profiling/"+FuncName+".dat")


    with open("Profiling/"+FuncName+"_time.txt",'w') as f:
        p = pstats.Stats(FuncName + ".dat",stream=f)
        p.sort_stats("time").print_stats()

    with open("Profiling/"+FuncName+"_calls.txt",'w') as f:
        p = pstats.Stats(FuncName + ".dat",stream=f)
        p.sort_stats("calls").print_stats()