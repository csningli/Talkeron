#! /usr/bin/

if __name__ == "__main__" :
    import sys, os, subprocess, time
    sys.path.append("/Users/nil/.talkeron/Actions/Common")
    import utils

    print("Execution of eurofootball.py started.")

    success, workPos, parasDic = utils.handle_sys_argv(sys.argv)

    if success is not True :
        exit(1)

    winOdd = parasDic.get("win", None)
    drawOdd = parasDic.get("draw", None)
    loseOdd = parasDic.get("lose", None)

    if winOdd is not None :
        print("Win odd: %.4f" % float(winOdd))
    else :
        print("Exit. [Input parameter \"win\" is missing or inavailable.]")
        exit(1)

    if drawOdd is not None :
        print("Draw odd: %.4f" % float(drawOdd))
    else :
        print("Exit. [Input parameter \"draw\" is missing or inavailable.]")
        exit(1)

    if loseOdd is not None :
        print("Lose odd: %.4f" % float(loseOdd))
    else :
        print("Exit. [Input parameter \"lose\" is missing or inavailable.]")
        exit(1)

    s = 0.0
    for odd in [winOdd, drawOdd, loseOdd] :
        if float(odd) > 0.1 and float(odd) < 100.0 :
            s += 1.0 / float(odd)

    if s > 1.00001 :
        delta = 1.0 - 1.0 / float(s)

        resultFileName = workPos + "/result.txt"

        with open(resultFileName, 'w') as f :
            f.write("Delta: %.4f; " % delta)
            f.write("Win prob: %.4f; " % ((1.0 - float(delta)) / float(winOdd)))
            f.write("Draw prob: %.4f; " % ((1.0 - float(delta)) / float(drawOdd)))
            f.write("Lose prob: %.4f; " % ((1.0 - float(delta)) / float(loseOdd)))
    else :
        print("Odds error with inversed summation: %.4f" % s)

    print("Done.")
