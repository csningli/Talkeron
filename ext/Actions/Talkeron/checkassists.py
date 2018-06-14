#! /usr/bin/


if __name__ == "__main__" :
    import sys, os, time, subprocess
    
    if len(sys.argv) < 2 :
        print("Exit. [There is not enough argument. Usage: python checkassists.py path/to/work_position]")
        exit(1)

    print("Execution of checkassists.py started.")
    
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
    backupPos = None
    dirToBk = None

    with open(inputFileName, 'r') as f :
        for line in f :
            lineSplit = line.split("\t")
            if lineSplit[0].strip() == "talkeron" and len(lineSplit) > 1:
                talkeronHome = lineSplit[1].strip() 

    talkeronAssists = talkeronHome + "/Assists"
    if talkeronHome is not None and os.path.isdir(talkeronAssists) :
        print("Talkeron home: ", talkeronHome)
    else :
        print("Exit. [Input parameter \"talkeron\" is missing or \"TalkeronHome/Assists\" inavailable.]")
        exit(1)
        
    resultFileName = workPos + "/result.txt"

    with open(resultFileName, 'w') as f :
        for dirname, dirnames, filenames in os.walk(talkeronAssists) :
            if (dirname == talkeronAssists) : 
                for subdirname in dirnames :
                    f.write("[" + subdirname + "] \n")
      
    print("Done.")
