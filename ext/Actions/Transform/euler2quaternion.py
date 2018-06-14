
import math

def quat_from_euler(roll, pitch, yaw) :
    q = [0.0, 0.0, 0.0, 0.0]
    t0 = math.cos(yaw * math.pi / 360.0)
    t1 = math.sin(yaw * math.pi / 360.0)
    t2 = math.cos(roll * math.pi / 360.0)
    t3 = math.sin(roll * math.pi / 360.0)
    t4 = math.cos(pitch * math.pi / 360.0)
    t5 = math.sin(pitch * math.pi / 360.0)
    q[0] = t0 * t2 * t4 + t1 * t3 * t5 
    q[1] = t0 * t3 * t4 - t1 * t2 * t5 
    q[2] = t0 * t2 * t5 + t1 * t3 * t4 
    q[3] = t1 * t2 * t4 - t0 * t3 * t5 
    return q

if __name__ == "__main__" :
    import sys, os, subprocess
    if len(sys.argv) < 2 :
        print("Exit. [There is not enough argument. Usage: python euler2quaternion.py path/to/work_position]")
        exit(1)

    print("Execution of euler2quaternion.py started.")
    
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
    pitch = None
    yaw = None
    roll = None
    
    with open(inputFileName, 'r') as f :
        for line in f :
            lineSplit = line.split("\t")
            if lineSplit[0].strip() == "talkeron" and len(lineSplit) > 1:
                talkeronHome = lineSplit[1].strip() 
            if lineSplit[0].strip() == "roll" and len(lineSplit) > 1:
                roll = float(lineSplit[1].strip())
            if lineSplit[0].strip() == "pitch" and len(lineSplit) > 1:
                pitch = float(lineSplit[1].strip())
            if lineSplit[0].strip() == "yaw" and len(lineSplit) > 1:
                yaw = float(lineSplit[1].strip())

    if roll is not None :
        print("Roll: ", roll)
    else :
        print("Exit. [Input parameter \"roll\" is missing or invalid.]")
        exit(1)
        
    if pitch is not None :
        print("Pitch: ", pitch)
    else :
        print("Exit. [Input parameter \"pitch\" is missing or invalid.]")
        exit(1)
    
    if yaw is not None :
        print("Yaw: ", yaw)
    else :
        print("Exit. [Input parameter \"yaw\" is missing or invalid.]")
        exit(1)
        
        
    resultFileName = workPos + "/result.txt"
    
    quaternion = quat_from_euler(roll, pitch, yaw) 
    
    print("Quaternion: ", quaternion)
    with open(resultFileName, 'w') as f :
        f.write(str(quaternion))
        
    print("Done.")
