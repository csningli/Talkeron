
import math
from quaternions import Quaternion

def quat_mul(p, q) :
    puat = Quaternion(p[0], p[1], p[2], p[3]) 
    quat = Quaternion(q[0], q[1], q[2], q[3]) 
    m = puat * quat
    return (m.w, m.x, m.y, m.z) 
    

if __name__ == "__main__" :
    import sys, os, subprocess
    if len(sys.argv) < 2 :
        print("Exit. [There is not enough argument. Usage: python quaternion2angleaxis.py path/to/work_position]")
        exit(1)

    print("Execution of quaternion2angleaxis.py started.")
    
    workPos = sys.argv[1]
    if os.path.isdir(workPos) :
        print("Detected work position:", workPos)
    else :
        print("Exit. [Work position:", workPos, "does not exist.]")
        exit(1)
        

    inputFileName = workPos + "/input.txt"

    if os.path.exists(inputFileName) :
        print("Detected input file: ", inputFileName)
    else :
        print("Exit. [Input file:", inputFileName, "does not exist.]")
        exit(1)


    talkeronHome = None
    p = None
    q = None
    
    with open(inputFileName, 'r') as f :
        for line in f :
            lineSplit = line.split("\t")
            if lineSplit[0].strip() == "talkeron" and len(lineSplit) > 1:
                talkeronHome = lineSplit[1].strip() 
            if lineSplit[0].strip() == "p" and len(lineSplit) > 1:
                pl = lineSplit[1].strip().split(' ')
                p = (float(pl[0].strip(", ")), float(pl[1].strip(", ")), float(pl[2].strip(", ")), float(pl[3].strip(", ")))
            if lineSplit[0].strip() == "q" and len(lineSplit) > 1:
                ql = lineSplit[1].strip().split(' ')
                q = (float(ql[0].strip(", ")), float(ql[1].strip(", ")), float(ql[2].strip(", ")), float(ql[3].strip(", ")))

    if p is not None :
        print("p: ", p)
    else :
        print("Exit. [Input parameter \"p\" is missing or invalid.]")
        exit(1)
        
    if q is not None :
        print("q: ", q)
    else :
        print("Exit. [Input parameter \"q\" is missing or invalid.]")
        exit(1)

    resultFileName = workPos + "/result.txt"
    
    m = quat_mul(p, q) 
    line = "result: (%f, %f, %f, %f) " % (m[0], m[1], m[2], m[3])
    print(line)
    with open(resultFileName, 'w') as f :
        f.write(line)

    print("Done.")
