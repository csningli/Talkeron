#! /usr/bin/

import sys, os, subprocess, time
    
def handle_sys_argv(sys_argv) :
   
    sucess = False 
    workPos = ""
    parasDict = {}
    
    if len(sys.argv) >= 2 :
        workPos = sys.argv[1]
        if os.path.isdir(workPos) :
            print("Detected work position:", workPos)
            inputFileName = workPos + "/input.txt"
            if os.path.exists(inputFileName) :
                print("Detected input file: ", inputFileName)
                with open(inputFileName, 'r') as f :
                    for line in f :
                        lineSplit = line.split("\t")
                        if len(lineSplit) > 1:
                            parasDict[lineSplit[0].strip()] = lineSplit[1].strip()
                sucess = True
            else :
                print("Exit. [Input file:", inputFileName, "does not exist.]")
        else :
            print("Exit. [Work position:", workPos, "does not exist.]")
    else :
        print("Exit. [There is not enough argument. Usage: python <script_name>.py path/to/work_position]")
    
    return sucess, workPos, parasDict
