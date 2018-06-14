#include "mainwindow.h"

#include<QSizeGrip>
#include<QDebug>
#include<QScrollBar>
#include<QTime>
#include<QPushButton>
#include<QLine>
#include <QDir>


#include"ui_mainwindow.h"
#include"cmdtextedit.h"
#include"taskblock.h"
#include"cmdcompileresult.h"
#include"talkerxml.h"



MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->tasksScroll->layout()->setAlignment(Qt::AlignTop);

    connect(ui->cmdEdit, &CmdTextEdit::enterPressed, this, &MainWindow::handleCmdInput);
    connect(ui->scrollArea->verticalScrollBar(), SIGNAL(rangeChanged(int,int)), this, SLOT(areaChanged(int,int)));
    init();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::init() {
    // look for TalkeronHome under HOME

    //qDebug() << "Home: " << QDir().homePath();

    talkConfig.home = QDir().homePath() + "/.talkeron";
    talkConfig.running = talkConfig.home + "/Running";
    talkConfig.assists = talkConfig.home + "/Assists";
    talkConfig.actions = talkConfig.home + "/Actions";
    talkConfig.history = talkConfig.home + "/history.txt";

    talkConfig.startdate = QDate().currentDate().toString("yyMMdd");
    talkConfig.starttime = QTime().currentTime().toString("HHmmss");

    //qDebug() << "Date: " << talkConfig.startdate;
    //qDebug() << "Time: " << talkConfig.starttime;


    if (! QDir().exists(talkConfig.home)) {
        //qDebug() << "Initialize home.";
        QDir().mkdir(talkConfig.home);
    }
    if (! QDir().exists(talkConfig.running)) {
        QDir().mkdir(talkConfig.running);
    }
    if (! QDir().exists(talkConfig.assists)) {
        QDir().mkdir(talkConfig.assists);
    }
    if (! QDir().exists(talkConfig.actions)) {
        QDir().mkdir(talkConfig.actions);
    }

    talkConfig.timelabel = 0;

    int currentHours = QTime().currentTime().toString("HH").toInt();
    if (0 <= currentHours and currentHours < 12) {
        ui->historyBrowser->append("[" + QTime().currentTime().toString() + " <font color=\"blue\">Success</font>] Good morning! Have a nice day!");
    } else if (12 <= currentHours and currentHours < 14) {
        ui->historyBrowser->append("[" + QTime().currentTime().toString() + " <font color=\"blue\">Success</font>] Good noon!");
    } else if (14 <= currentHours and currentHours < 18) {
        ui->historyBrowser->append("[" + QTime().currentTime().toString() + " <font color=\"blue\">Success</font>] Good afternoon!");
    } else if (18 <= currentHours and currentHours <= 24) {
        ui->historyBrowser->append("[" + QTime().currentTime().toString() + " <font color=\"blue\">Success</font>] Good evening!");
    } else {
        ui->historyBrowser->append("[" + QTime().currentTime().toString() + " <font color=\"blue\">Success</font>] Welcome!");
    }

    ui->cmdEdit->loadMemory(talkConfig.history);
}

void MainWindow::handleCmdInput() {
     QString cmd = QString(ui->cmdEdit->toPlainText());

     CmdCompileResult *r = compileCmd(cmd);
     if (r != 0) {
        if (r->getCompiled()) {
            ui->historyBrowser->append("[" + QTime().currentTime().toString() + " <font color=\"blue\">Success</font>] " + cmd);
            ui->cmdEdit->addMemory();
        } else {
            ui->historyBrowser->append("[" + QTime().currentTime().toString() + " <font color=\"red\">Failed</font>] " + r->getComment());
        }
     } else {
        ui->historyBrowser->append("[" + QTime().currentTime().toString() + " <font color=\"red\">Compile error.</font>] ");
     }
}

CmdCompileResult* MainWindow::compileCmd(QString cmd){

    CmdCompileResult* r = new CmdCompileResult();

    QStringList cmdParts = cmd.split(" ");
    QString assistXmlPath = talkConfig.assists + "/" + (cmdParts[0].split(".")).join("/") + "/" + (cmdParts[0].split(".").last() + ".talk");
    //qDebug() << "AssistXmlPath: " << assistXmlPath;

    if (QFile().exists(assistXmlPath)) {
        createTask(cmd);
        r->setCompiled(true);
        r->setComment("Proper command");
    } else {
        r->setCompiled(false);
        r->setComment("Cannot find the assist.");
    }

    return  r;
}

 void MainWindow::createTask(QString cmd) {
     TaskBlock *task = new TaskBlock();
     task->cmdEdit = ui->cmdEdit;
     QStringList cmdParts = cmd.split(" ");

     task->assistName = cmdParts[0];
     task->assistsPos = talkConfig.assists + "/" + (cmdParts[0].split(".")).join("/");
     task->assistXmlPath = task->assistsPos + "/" + task->assistName.split(".").last() + ".talk";

     for (int i = 1; i < cmdParts.length(); i++) {
         task->runningParas << cmdParts[i];
     }

     task->init();

     ui->tasksScroll->layout()->addWidget(task);

    return;
 }

 void MainWindow::areaChanged(int min, int max) {
     Q_UNUSED(min);
     ui->scrollArea->verticalScrollBar()->setValue(max);
 }

 void MainWindow::closeEvent(QCloseEvent *event) {
      // do some data saves or something else
     ui->cmdEdit->saveMemory(talkConfig.history);
     QMainWindow::closeEvent(event);
 }


