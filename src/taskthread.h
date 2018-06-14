#ifndef TASKTHREAD_H
#define TASKTHREAD_H

#include<QThread>

#include"taskblock.h"

class TaskThread : public QThread
{
    Q_OBJECT

public:
    QString workpos;
    QString cmdline;
    TaskBlock *task;

    TaskThread();

protected :
    void run();

};

#endif // TASKTHREAD_H
