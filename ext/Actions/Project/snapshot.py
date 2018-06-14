#! /usr/bin/


if __name__ == "__main__" :
    import sys, os, time, subprocess
    
    if len(sys.argv) < 2 :
        print("Exit. [There is not enough argument. Usage: python snapshot.py path/to/work_position]")
        exit(1)

    print("Execution of snapshot.py started.")
    
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
    dirToBk = None

    with open(inputFileName, 'r') as f :
        for line in f :
            lineSplit = line.split("\t")
            if lineSplit[0].strip() == "projpath" and len(lineSplit) > 1:
                dirToBk = lineSplit[1].strip() 
            if lineSplit[0].strip() == "shotpos" and len(lineSplit) > 1 :
                shotPos = lineSplit[1].strip()
            if lineSplit[0].strip() == "talkeron" and len(lineSplit) > 1 :
                talkeronHome = lineSplit[1].strip() 

    if dirToBk is not None and os.path.isdir(dirToBk) :
        print("Directory to snapshot: ", dirToBk)
    else :
        print("Exit. [Input parameter \"projpath\" is missing or inavailable.]")
        exit(1)
        
    if shotPos is not None and os.path.isdir(shotPos) :
        print("Snapshots position: ", shotPos)
    else :
        print("Exit. [Input parameter \"shotpos\" is missing or inavailable.]")
        exit(1)
    
    resultFileName = workPos + "/result.txt"

    projectName = dirToBk.strip().split("/")[-1]

    os.chdir(dirToBk)
    snapshotName = dirToBk.strip().split("/")[-1] + "-" +  time.strftime("%y%m%d%H%M%S") + ".zip"
    cmd = "zip -r " + snapshotName + " ./* --exclude=*.fslckout*" 
    subprocess.call(cmd, shell=True)
    cmd = "mv ./" + snapshotName + " " + shotPos + "/" + snapshotName 
    subprocess.call(cmd, shell=True)
    
    print("Done.")
