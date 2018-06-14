
import math

def euler_from_quat(q) :
    t0 = 2.0 * (q[0] * q[1] + q[2] * q[3])
    t1 = 1.0 - 2.0 * (q[1] * q[1] + q[2] * q[2])
    roll = math.atan2(t0, t1) * 180.0 / math.pi

    t2 = 2.0 * (q[0] * q[2] - q[3] * q[1])
    if t2 > 1.0 :
        t2 = 1.0
    if t2 < -1.0 :
        t2 = -1.0
    pitch = math.asin(t2) * 180.0 / math.pi

    t3 = 2.0 * (q[0] * q[3] + q[1] * q[2])
    t4 = 1.0 - 2.0 * (q[2] * q[2] + q[3] * q[3])
    yaw = math.atan2(t3, t4) * 180.0 / math.pi
    
    return (roll, pitch, yaw)

if __name__ == "__main__" :
    import sys, os, subprocess
    if len(sys.argv) < 2 :
        print("Exit. [There is not enough argument. Usage: python quaternion2euler.py path/to/work_position]")
        exit(1)

    print("Execution of quaternion2euler.py started.")
    
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
    
    euler = euler_from_quat([q0, q1, q2, q3]) 
    
    print("[roll, pitch, yaw]: ", euler)
    with open(resultFileName, 'w') as f :
        f.write("[roll, pitch, yaw]: " + str(euler))

    print("Done.")
