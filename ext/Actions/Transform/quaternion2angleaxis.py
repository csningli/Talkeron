
import math
from quaternions import Quaternion

def quat_2_angle_axis(q) :
    quat = Quaternion(q[0], q[1], q[2], q[3]) 
    angle = 2 * math.acos(quat.w) / math.pi * 180.0
    s = math.sqrt(1 - quat.w * quat.w)
    x = quat.x
    y = quat.y
    z = quat.z
    if s > 0.000001 :
        x = quat.x / s
        y = quat.y / s
        z = quat.z / s
    return (angle, x, y, z)
    

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
    q0 = None
    q1 = None
    q2 = None
    q3 = None
    
    with open(inputFileName, 'r') as f :
        for line in f :
            lineSplit = line.split("\t")
            if lineSplit[0].strip() == "talkeron" and len(lineSplit) > 1:
                talkeronHome = lineSplit[1].strip() 
            if lineSplit[0].strip() == "q0" and len(lineSplit) > 1:
                q0 = float(lineSplit[1].strip())
            if lineSplit[0].strip() == "q1" and len(lineSplit) > 1:
                q1 = float(lineSplit[1].strip())
            if lineSplit[0].strip() == "q2" and len(lineSplit) > 1:
                q2 = float(lineSplit[1].strip())
            if lineSplit[0].strip() == "q3" and len(lineSplit) > 1:
                q3 = float(lineSplit[1].strip())

    if q0 is not None :
        print("Quaternion[0]: ", q0)
    else :
        print("Exit. [Input parameter \"q0\" is missing or invalid.]")
        exit(1)
        
    if q1 is not None :
        print("Quaternion[1]: ", q1)
    else :
        print("Exit. [Input parameter \"q1\" is missing or invalid.]")
        exit(1)
        
    if q2 is not None :
        print("Quaternion[2]: ", q2)
    else :
        print("Exit. [Input parameter \"q2\" is missing or invalid.]")
        exit(1)
        
    if q3 is not None :
        print("Quaternion[3]: ", q3)
    else :
        print("Exit. [Input parameter \"q3\" is missing or invalid.]")
        exit(1)

    resultFileName = workPos + "/result.txt"
    
    aa = quat_2_angle_axis([q0, q1, q2, q3]) 
    
    line = "angle: %f; axis: (%f, %f, %f) " % (aa[0], aa[1], aa[2], aa[3])
    print(line)
    with open(resultFileName, 'w') as f :
        f.write(line)

    print("Done.")
