#! /usr/bin/


if __name__ == "__main__" :
    import sys, os, time, subprocess
    
    if len(sys.argv) < 2 :
        print("Exit. [There is not enough argument. Usage: python fossilclone.py path/to/work_position]")
        exit(1)

    print("Execution of fossilclone.py started.")
    
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
    backupRep = None
    dirToDeploy = None

    with open(inputFileName, 'r') as f :
        for line in f :
            lineSplit = line.split("\t")
            if lineSplit[0].strip() == "project" and len(lineSplit) > 1:
                dirToDeploy = lineSplit[1].strip() 
            if lineSplit[0].strip() == "repository" and len(lineSplit) > 1:
                backupRep = lineSplit[1].strip() 
            if lineSplit[0].strip() == "talkeron" and len(lineSplit) > 1:
                talkeronHome = lineSplit[1].strip() 

    if dirToDeploy is not None and not os.path.isdir(dirToDeploy) :
        print("Directory to deploy: ", dirToDeploy)
    else :
        print("Exit. [Input parameter \"project\" is missing or it already exist.]")
        exit(1)
        
    if backupRep is not None and os.path.exists(backupRep) :
        print("Repository to deploy: ", backupRep)
    else :
        print("Exit. [Input parameter \"repository\" is missing or inavailable.]")
        exit(1)
    
    resultFileName = workPos + "/result.txt"

    os.mkdir(dirToDeploy)
    os.chdir(dirToDeploy)
    cmd = "/Applications/fossil user default nil"
    subprocess.call(cmd, shell=True)
    cmd = "/Applications/fossil open " + backupRep
    subprocess.call(cmd, shell=True)
    
    
    print("Done.")
