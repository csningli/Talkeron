#! /usr/bin/


if __name__ == "__main__" :
    import sys, os, subprocess
    if len(sys.argv) < 2 :
        print("Exit. [There is not enough argument. Usage: python assist.py path/to/work_position]")
        exit(1)

    print("Execution of assist.py started.")
    
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
    projectName = None
    
    with open(inputFileName, 'r') as f :
        for line in f :
            lineSplit = line.split("\t")
            if lineSplit[0].strip() == "talkeron" and len(lineSplit) > 1:
                talkeronHome = lineSplit[1].strip() 
            if lineSplit[0].strip() == "projname" and len(lineSplit) > 1:
                projectName = lineSplit[1].strip()

    talkeronAssists = talkeronHome + "/Assists" 
    if talkeronHome is not None and os.path.isdir(talkeronAssists) :
        print("Directory of Talkeron assists: ", talkeronAssists)
    else :
        print("Exit. [Input parameter \"talkeron\" is missing or \"TalkeronHome/Assists\" inavailable.]")
        exit(1)
        
    resultFileName = workPos + "/result.txt"
    
    projectAssist = talkeronAssists + "/" + projectName 

    if not os.path.isdir(projectAssist) :
        print(projectAssist, "does not exist. Create one.")
        os.mkdir(projectAssist)
    
        # create the directory of the assist
        assistConfigFile = projectAssist + "/" + projectName +  ".talk"

        with open(assistConfigFile, 'w') as f :
            f.write("<?xml version = \"1.0\" ?>\n")
            f.write("<assist>\n")
            f.write("\t<desc>" + projectName + "</desc>\n")
            f.write("\t<comment></comment>\n")
            f.write("\t<para>\n")
            f.write("\t\t<name></name>\n")
            f.write("\t\t<type></type>\n")
            f.write("\t\t<range></range>\n")
            f.write("\t\t<value></value>\n")
            f.write("\t</para>\n")
            f.write("\t<action>\n")
            f.write("\t\t<run></run>\n")
            f.write("\t\t<redo></redo>\n")
            f.write("\t\t<undo></undo>\n")
            f.write("\t</action>\n")
            f.write("\t<hand></hand>\n")
            f.write("</assist>\n")
    
        
    print("Done.")
