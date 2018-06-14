#! /usr/bin/


if __name__ == "__main__" :
    import sys, os, subprocess, base64
    if len(sys.argv) < 2 :
        print("Exit. [There is not enough argument. Usage: python base64encode.py path/to/work_position]")
        exit(1)

    print("Execution of base64encode.py started.")
    
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
    imgPath = None
    
    with open(inputFileName, 'r') as f :
        for line in f :
            lineSplit = line.split("\t")
            if lineSplit[0].strip() == "talkeron" and len(lineSplit) > 1:
                talkeronHome = lineSplit[1].strip() 
            if lineSplit[0].strip() == "imgpath" and len(lineSplit) > 1:
                imgPath = lineSplit[1].strip()

    if imgPath is not None and os.path.exists(imgPath) :
        print("Image: ", imgPath)
    else :
        print("Exit. [Input parameter \"image\" is missing or inavailable.]")
        exit(1)
    
    resultFileName = workPos + "/result.txt"

    encoded_string = base64.b64encode(open(imgPath, "rb").read())
    
    print("Base64 code here: [" + encoded_string + "]")
    print("Add img label with src=\"data:image/png;base64,[code]\" to your html file.")

    with open(resultFileName, 'w') as f :
        f.write("Base64 code here: [" + encoded_string + "]. Add img label with src=\"data:image/png;base64,[code]\" to your html file.")

    print("Done.")
