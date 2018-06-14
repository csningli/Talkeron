
import math
from quaternions import Quaternion
from quaternion2angleaxis import quat_2_angle_axis

def angle_axis_mul(a, b) :
    qa = Quaternion.from_axis_angle([a[1], a[2], a[3]], a[0] / 180.0 * math.pi)
    qb = Quaternion.from_axis_angle([b[1], b[2], b[3]], b[0] / 180.0 * math.pi)
    m = qa * qb
    aa = quat_2_angle_axis((m.w, m.x, m.y, m.z))
    return (aa[0], aa[1], aa[2], aa[3]) 
    

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
    a = None
    b = None
    
    with open(inputFileName, 'r') as f :
        for line in f :
            lineSplit = line.split("\t")
            if lineSplit[0].strip() == "talkeron" and len(lineSplit) > 1:
                talkeronHome = lineSplit[1].strip() 
            if lineSplit[0].strip() == "a" and len(lineSplit) > 1:
                al = lineSplit[1].strip().split(' ')
                a = (float(al[0].strip(", ")), float(al[1].strip(", ")), float(al[2].strip(", ")), float(al[3].strip(", ")))
            if lineSplit[0].strip() == "b" and len(lineSplit) > 1:
                bl = lineSplit[1].strip().split(' ')
                b = (float(bl[0].strip(", ")), float(bl[1].strip(", ")), float(bl[2].strip(", ")), float(bl[3].strip(", ")))

    if a is not None :
        print("a: ", a)
    else :
        print("Exit. [Input parameter \"a\" is missing or invalid.]")
        exit(1)
        
    if b is not None :
        print("b: ", b)
    else :
        print("Exit. [Input parameter \"b\" is missing or invalid.]")
        exit(1)

    resultFileName = workPos + "/result.txt"
    
    aa = angle_axis_mul(a, b) 
    line = "angle: %f; axis: (%f, %f, %f) " % (aa[0], aa[1], aa[2], aa[3])
    print(line)
    with open(resultFileName, 'w') as f :
        f.write(line)

    print("Done.")
