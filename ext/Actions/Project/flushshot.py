#! /usr/bin/


if __name__ == "__main__" :
    import sys, os, time, subprocess
    
    if len(sys.argv) < 2 :
        print("Exit. [There is not enough argument. Usage: python flushshot.py path/to/work_position]")
        exit(1)

    print("Execution of flushshot.py started.")
    
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
    shotPos = None
    shotName = None
    dirToFlush = None

    with open(inputFileName, 'r') as f :
        for line in f :
            lineSplit = line.split("\t")
            if lineSplit[0].strip() == "projpath" and len(lineSplit) > 1:
                dirToFlush = lineSplit[1].strip() 
            if lineSplit[0].strip() == "shotpos" and len(lineSplit) > 1 :
                shotPos = lineSplit[1].strip()
            if lineSplit[0].strip() == "shotname" and len(lineSplit) > 1 :
                shotName = lineSplit[1].strip()
            if lineSplit[0].strip() == "talkeron" and len(lineSplit) > 1 :
                talkeronHome = lineSplit[1].strip() 

    if dirToFlush is not None and os.path.isdir(dirToFlush) :
        print("Directory to flush: ", dirToFlush)
    else :
        print("Exit. [Input parameter \"projpath\" is missing or inavailable.]")
        exit(1)
        
    if shotPos is not None and os.path.exists(shotPos + "/" + shotName) :
        print("Snapshot: ", shotPos + "/" + shotName)
    else :
        print("Exit. [Input parameter \"shotpos\" is missing or the snapshot " + shotPos + "/" + shotName + " inavailable.]")
        exit(1)
    
    resultFileName = workPos + "/result.txt"

    projectName = dirToFlush.strip().split("/")[-1]

    os.chdir(dirToFlush)
    cmd = "unzip -o " + shotPos + "/" + shotName 
    subprocess.call(cmd, shell=True)

    print("Done.")
