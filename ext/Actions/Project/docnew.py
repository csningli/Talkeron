#! /usr/bin/


if __name__ == "__main__" :
    import sys, os, subprocess, time
    if len(sys.argv) < 2 :
        print("Exit. [There is not enough argument. Usage: python docnew.py path/to/work_position]")
        exit(1)

    print("Execution of docnew.py started.")
    
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
        print("Exit. [Input parameter \"projpath\" is missing or inavailable.]")
        exit(1)
    
    os.chdir(projectPath)
    
    with open("./" + time.strftime("%y%m%d%H%M%S") + "-newdoc.html", 'w') as f :
        f.write("<html>\n")    
        f.write("<head>\n")    
        f.write("<script type=\"text/javascript\" src=\"http://latex.codecogs.com/latexit.js\"></script>\n")
        f.write("<script type=\"text/javascript\">LatexIT.add('p', true);</script>\n")
        f.write("</head>\n")    
        f.write("<body>\n")    
        f.write("<div style=\"width:600px\">\n")    
        f.write("<h2> Topic </h2> topic\n")    
        f.write("<hr>\n")    
        f.write("<h2> Comment </h2> comment\n")    
        f.write("<hr>\n")    
        f.write("<h2> Content </h2>\n")    
        f.write("<p>\n")    
        f.write("content\n")    
        f.write("</p>\n")    
        f.write("</div>\n")    
        print("Now you can edit the new doc file under the project root.")
    
    print("Done.")
