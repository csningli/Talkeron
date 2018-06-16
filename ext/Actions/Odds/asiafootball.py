#! /usr/bin/

if __name__ == "__main__" :
    import sys, os, subprocess, time
    sys.path.append("/Users/nil/.talkeron/Actions/Common")
    import utils

    print("Execution of asiafootball.py started.")

    success, workPos, parasDic = utils.handle_sys_argv(sys.argv)

    if success is not True :
        exit(1)

    upOdd = parasDic.get("up", None)
    downOdd = parasDic.get("down", None)

    if upOdd is not None :
        print("Up odd: %.4f" % float(upOdd))
    else :
        print("Exit. [Input parameter \"up\" is missing or inavailable.]")
        exit(1)

    if downOdd is not None :
        print("Down odd: %.4f" % float(downOdd))
    else :
        print("Exit. [Input parameter \"down\" is missing or inavailable.]")
        exit(1)

    s = 0.0
    for odd in [upOdd, downOdd, ] :
        if float(odd) > 0.1 and float(odd) < 2.0 :
            s += 1.0 / float(1.0 + float(odd))

    if s > 1.00001 :
        delta = 1.0 - 1.0 / float(s)

        resultFileName = workPos + "/result.txt"

        with open(resultFileName, 'w') as f :
            f.write("Delta: %.4f; " % delta)
            f.write("Up prob: %.4f; " % ((1.0 - float(delta)) / (1.0 + float(upOdd))))
            f.write("Down prob: %.4f; " % ((1.0 - float(delta)) / (1.0 + float(downOdd))))
    else :
        print("Odds error with inversed summation: %.4f" % s)

    print("Done.")
