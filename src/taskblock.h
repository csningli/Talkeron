#ifndef TASKBLOCK_H
#define TASKBLOCK_H

//#include"mainwindow.h"

#include<QMainWindow>
#include<QWidget>
#include<QTextBrowser>
#include<QPushButton>
#include <QXmlStreamReader>

#include"cmdtextedit.h"

struct Hand {
    QString desc;
};

struct Para {
    QString name;
    QString type;
    QString range;
    QString value;
};

class TaskBlock : public QWidget
{

public:
    QString assistsPos = "";
    QString assistXmlPath = "";
    QString assistName = "";

    QStringList runningParas;
    QStringList paraNames;

    QString runCmd = "";
    QString redoCmd = "";
    QString undoCmd = "";

    QTextBrowser *result = 0;
    QTextBrowser *stdoutput = 0;
    QTextBrowser *stderror = 0;

    CmdTextEdit *cmdEdit;

    TaskBlock();
    void init();
    QWidget* createLine();
    void prepareWorkPos(QString workPos);



public slots :
    void executeHand();
    void openResult();
    void openStdOutput();
    void openStdError();
    void openAssistFolder();
    void updateResult();
    void refreshResult();

private slots:
    void resultAreaChanged(int, int);
    void stdoutputAreaChanged(int, int);
    void stderrorAreaChanged(int, int);

private :
    //QMainWindow *userinterface;
    int _lineAbility;
    QString _lastEntryType;
    QWidget *_currentLine;
    void xmlParseAction(QXmlStreamReader &xml);
    void xmlParsePara(QXmlStreamReader &xml);
    void xmlParseHand(QXmlStreamReader &xml);
};


#endif // TASKBLOCK_H
