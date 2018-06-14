#! /usr/bin/


if __name__ == "__main__" :
    import sys, os, subprocess
    if len(sys.argv) < 2 :
        print("Exit. [There is not enough argument. Usage: python open.py path/to/work_position]")
        exit(1)

    print("Execution of open.py started.")
    
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
    projectPath = None
    
    with open(inputFileName, 'r') as f :
        for line in f :
            lineSplit = line.split("\t")
            if lineSplit[0].strip() == "talkeron" and len(lineSplit) > 1:
                talkeronHome = lineSplit[1].strip() 
            if lineSplit[0].strip() == "projpath" and len(lineSplit) > 1:
                projectPath = lineSplit[1].strip()

    if projectPath is not None and os.path.isdir(projectPath) :
        print("Project: ", projectPath)
    else :
        print("Exit. [Input parameter \"project\" is missing or inavailable.]")
        exit(1)
    
       
    cmd = "open " + projectPath
    subprocess.call(cmd, shell = True)
    
    print("Done.")
