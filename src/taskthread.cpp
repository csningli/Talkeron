#include "taskthread.h"
#include<QProcess>
#include<QDebug>


TaskThread::TaskThread()
{
    workpos = "";
    cmdline = "";
    task = 0;
}

void TaskThread::run()
{
    if (workpos != "" and cmdline != "") {
        // execute the command line
        QProcess *proc = new QProcess();
        proc->setStandardOutputFile(workpos + "/output.txt");
        proc->setStandardErrorFile(workpos + "/error.txt");
        proc->start(cmdline + " " + workpos);

        return;
    }
}
