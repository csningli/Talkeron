#! /usr/bin/


if __name__ == "__main__" :
    import sys, os, time, subprocess
    
    if len(sys.argv) < 2 :
        print("Exit. [There is not enough argument. Usage: python fossilbk.py path/to/work_position]")
        exit(1)

    print("Execution of fossilbk.py started.")
    
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
    fossilPath = None 
    backupPos = None
    dirToBk = None
    msg = None

    with open(inputFileName, 'r') as f :
        for line in f :
            lineSplit = line.split("\t")
            if lineSplit[0].strip() == "projpath" and len(lineSplit) > 1 :
                dirToBk = lineSplit[1].strip() 
            if lineSplit[0].strip() == "fossil" and len(lineSplit) > 1 :
                fossilPath = lineSplit[1].strip() 
            if lineSplit[0].strip() == "backup" and len(lineSplit) > 1 :
                backupPos = lineSplit[1].strip()
            if lineSplit[0].strip() == "talkeron" and len(lineSplit) > 1 :
                talkeronHome = lineSplit[1].strip() 
            if lineSplit[0].strip() == "message" and len(lineSplit) > 1 :
                msg = lineSplit[1].strip() 

    if dirToBk is not None and os.path.isdir(dirToBk) :
        print("Directory to backup: ", dirToBk)
    else :
        print("Exit. [Input parameter \"projpath\" is missing or inavailable.]")
        exit(1)
        
    if backupPos is not None and os.path.isdir(backupPos) :
        print("Backup position: ", backupPos)
    else :
        print("Exit. [Input parameter \"backup\" is missing or inavailable.]")
        exit(1)
    
    resultFileName = workPos + "/result.txt"

    projectName = dirToBk.strip().split("/")[-1]

    os.chdir(dirToBk)
    cmd = fossilPath + " user new nil nil@nil nilatfossil"
    subprocess.call(cmd, shell=True)
    cmd = fossilPath + " user default nil"
    subprocess.call(cmd, shell=True)
    if os.path.exists(dirToBk + "/.fslckout") :
        print("Target directory is already connected to some fossil repository. Refresh files and commit.")
        cmd = fossilPath + " addremove"
        subprocess.call(cmd, shell=True)
        cmd = fossilPath + " commit --no-warnings -m \"auto-committed_with_fossilbk.py: " + msg + "\""
        subprocess.call(cmd, shell=True)
    else :
        print("Create a new fossil repository and connect the target directory.")
        fossilRep = backupPos + "/" + time.strftime("%y%m%d%H%M%S") + "-" + dirToBk.strip().split("/")[-1] + ".fossil"
        cmd = fossilPath + " new " + fossilRep
        subprocess.call(cmd, shell=True)
        cmd = fossilPath + " open " + fossilRep
        subprocess.call(cmd, shell=True)
        cmd = fossilPath + " addremove"
        subprocess.call(cmd, shell=True)
        cmd = fossilPath + " commit --no-warnings -m \"fossil_repository_created_and_initialized.\""
        subprocess.call(cmd, shell=True)
    
    
    print("Done.")
