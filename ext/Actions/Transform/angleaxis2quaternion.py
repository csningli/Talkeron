
import math
from quaternions import Quaternion

def angle_axis_2_quat(angle, x, y, z) :
    q = Quaternion.from_axis_angle([x, y, z], angle / 180.0 * math.pi)
    return (q.w, q.x, q.y, q.z) 
    

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
    angle = None
    x = None
    y = None
    z = None
    
    with open(inputFileName, 'r') as f :
        for line in f :
            lineSplit = line.split("\t")
            if lineSplit[0].strip() == "talkeron" and len(lineSplit) > 1:
                talkeronHome = lineSplit[1].strip() 
            if lineSplit[0].strip() == "angle" and len(lineSplit) > 1:
                angle = float(lineSplit[1].strip())
            if lineSplit[0].strip() == "x" and len(lineSplit) > 1:
                x = float(lineSplit[1].strip())
            if lineSplit[0].strip() == "y" and len(lineSplit) > 1:
                y = float(lineSplit[1].strip())
            if lineSplit[0].strip() == "z" and len(lineSplit) > 1:
                z = float(lineSplit[1].strip())

    if angle is not None :
        print("angle: ", angle)
    else :
        print("Exit. [Input parameter \"angle\" is missing or invalid.]")
        exit(1)
        
    if x is not None :
        print("x: ", x)
    else :
        print("Exit. [Input parameter \"x\" is missing or invalid.]")
        exit(1)

    if y is not None :
        print("y: ", y)
    else :
        print("Exit. [Input parameter \"y\" is missing or invalid.]")
        exit(1)

    if z is not None :
        print("z: ", z)
    else :
        print("Exit. [Input parameter \"z\" is missing or invalid.]")
        exit(1)

    resultFileName = workPos + "/result.txt"
    
    q = angle_axis_2_quat(angle, x, y, z) 
    line = "quaternion: (%f, %f, %f, %f) " % (q[0], q[1], q[2], q[3])
    print(line)
    with open(resultFileName, 'w') as f :
        f.write(line)

    print("Done.")
