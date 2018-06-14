#include "taskblock.h"

#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QProcess>
#include <QDebug>
#include <QXmlStreamReader>
#include <QFile>
#include <QDir>
#include <QFileInfo>
#include <QLineEdit>

#include "mainwindow.h"
#include "taskthread.h"

#define TASKBLOCKLINE_H 100
#define TASKBUTTON_W 90
#define TASKLABEL_W 60
#define TASKFIELD_W 90
#define TASKWIDGET_H 25

extern MainWindow *mw;

TaskBlock::TaskBlock()
{
    this->setLayout(new QVBoxLayout);
    this->layout()->setAlignment(Qt::AlignTop);
    this->layout()->setSpacing(0);
    this->layout()->setMargin(1);
    this->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
    this->setStyleSheet("border-style: outset; border-width:2px; border-color: grey; background-color: white");

}

void TaskBlock::init()
{
    runCmd = "";
    redoCmd = "";
    undoCmd = "";

    //mw->connect(this->result->verticalScrollBar(), SIGNAL(rangeChanged(int,int)), this, SLOT(resultAreaChanged(int,int)));
    //mw->connect(this->stdoutput->verticalScrollBar(), SIGNAL(rangeChanged(int,int)), this, SLOT(this->stdoutputAreaChanged(int,int)));
    //mw->connect(this->stderror->verticalScrollBar(), SIGNAL(rangeChanged(int,int)), this, SLOT(this->stderrorAreaChanged(int,int)));

    _currentLine = createLine();                                // line with title
    _lineAbility = 3;
    QLabel *taskTitle = new QLabel();
    taskTitle->setText(assistName);
    taskTitle->setMaximumHeight(TASKWIDGET_H);
    _currentLine->layout()->addWidget(taskTitle);

    QPushButton *titleButton = new QPushButton();
    titleButton->setText("Open");
    titleButton->setFixedWidth(TASKBUTTON_W);
    titleButton->setStyleSheet("QPushButton {border-style: outset; border-width: 2px; background-color: grey; color: white;} QPushButton:pressed {background-color: white; color: grey}");
    connect(titleButton, &QPushButton::clicked, this, &TaskBlock::openAssistFolder);
    _currentLine->layout()->addWidget(titleButton);

    _lastEntryType = "Title";

    // parse the config.talk of assist

    QFile *configFile = new QFile(assistXmlPath);
    if (!configFile->open(QIODevice::ReadOnly | QIODevice::Text)) {
        return;
    }

    QXmlStreamReader xml(configFile);

    while (!xml.atEnd() and !xml.hasError()) {
        QXmlStreamReader::TokenType token = xml.readNext();
        if (token == QXmlStreamReader::StartDocument) {
            continue;
        }
        if (token == QXmlStreamReader::StartElement) {
            if (xml.name() == "desc") {
                xml.readNext();
                //qDebug() << "desc: " << xml.text().toString();
                if (xml.text().toString() != assistName) {
                    break;
                }
                continue;
            }
            if (xml.name() == "comment") {
                xml.readNext();
                //qDebug() << "comment: " << xml.text().toString();
                if (xml.text().toString().length() > 0) {
                    QLabel *taskComment = new QLabel();
                    taskComment->setText("[" + xml.text().toString() + "]");
                    taskComment->setMaximumHeight(TASKWIDGET_H);
                    _currentLine->layout()->addWidget(taskComment);
                }
                continue;
            }
            if (xml.name() == "action") {
                xmlParseAction(xml);
                //qDebug() << "run: " << runCmd;
                //qDebug() << "redo: " << redoCmd;
                //qDebug() << "undo: " << undoCmd;
                continue;
            }
            if (xml.name() == "para") {
                xmlParsePara(xml);
                continue;
            }
            if (xml.name() == "hand") {
                xmlParseHand(xml);
                continue;
            }
        }
    }

    for (int i = 0; i < runningParas.length(); i++) {
        QLineEdit *runningParaEdit = this->findChild<QLineEdit *>(runningParas[i].split("=")[0]);
        if (runningParaEdit != 0) {
            runningParaEdit->setText(runningParas[i].split("=")[1]);
        }
    }

    // add actions: run, redo and undo

    if (runCmd.length() > 0) {
        QFrame *separator = new QFrame();
        separator->setObjectName(QString::fromUtf8("line"));
        separator->setFrameShape(QFrame::HLine);
        separator->setFrameShadow(QFrame::Sunken);
        this->layout()->addWidget(separator);

        _currentLine = createLine();                             // line of default actions
        _lineAbility = 3;

        QPushButton *runButton = new QPushButton();
        runButton->setFixedWidth(TASKBUTTON_W);
        runButton->setText("Do");
        runButton->setObjectName("run");
        runButton->setToolTip(runCmd);
        runButton->setStyleSheet("QPushButton {border-style: outset; border-width: 2px; background-color: grey; color: white;} QPushButton:pressed {background-color: white; color: grey}");
        connect(runButton, &QPushButton::clicked, this, &TaskBlock::executeHand);
        _currentLine->layout()->addWidget(runButton);

        QPushButton *redoButton = new QPushButton();
        redoButton->setFixedWidth(TASKBUTTON_W);
        redoButton->setText("Redo");
        redoButton->setObjectName("redo");
        redoButton->setToolTip(redoCmd);
        redoButton->setStyleSheet("QPushButton {border-style: outset; border-width: 2px; background-color: grey; color: white;} QPushButton:pressed {background-color: white; color: grey}");
        connect(redoButton, &QPushButton::clicked, this, &TaskBlock::executeHand);
        _currentLine->layout()->addWidget(redoButton);
        redoButton->setVisible(false);

        QPushButton *undoButton = new QPushButton();
        undoButton->setFixedWidth(TASKBUTTON_W);
        undoButton->setText("Undo");
        undoButton->setObjectName("undo");
        undoButton->setToolTip(undoCmd);
        undoButton->setStyleSheet("QPushButton {border-style: outset; border-width: 2px; background-color: grey; color: white;} QPushButton:pressed {background-color: white; color: grey}");
        connect(undoButton, &QPushButton::clicked, this, &TaskBlock::executeHand);
        _currentLine->layout()->addWidget(undoButton);
        undoButton->setVisible(false);
    }
}

void TaskBlock::resultAreaChanged(int min, int max) {
    Q_UNUSED(min);
    //this->result->verticalScrollBar()->setValue(max);
}

void TaskBlock::stdoutputAreaChanged(int min, int max) {
    Q_UNUSED(min);
    //this->stdoutput->verticalScrollBar()->setValue(max);
}

void TaskBlock::stderrorAreaChanged(int min, int max) {
    Q_UNUSED(min);
    //this->stderror->verticalScrollBar()->setValue(max);
}


QWidget *TaskBlock::createLine() {
    QWidget *line = new QWidget();
    line->setMaximumHeight(TASKBLOCKLINE_H);
    line->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
    line->setLayout(new QHBoxLayout);
    line->layout()->setAlignment(Qt::AlignLeft);
    line->setStyleSheet("border-width:0px");
    this->layout()->addWidget(line);
    return line;
}

void TaskBlock::updateResult() {
    if (result == 0) {
        QWidget *line = this->createLine();

        QLabel *rLabel = new QLabel();
        rLabel->setText("Result :");
        rLabel->setMaximumHeight(TASKWIDGET_H);
        rLabel->setFixedWidth(TASKLABEL_W);
        rLabel->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
        rLabel->setStyleSheet("border-width:0px;");
        line->layout()->addWidget(rLabel);

        QPushButton *rButton = new QPushButton();
        rButton->setText("Open");
        rButton->setFixedWidth(TASKBUTTON_W);
        rButton->setStyleSheet("QPushButton {border-style: outset; border-width: 2px; background-color: grey; color: white;} QPushButton:pressed {background-color: white; color: grey}");        
        connect(rButton, &QPushButton::clicked, this, &TaskBlock::openResult);
        line->layout()->addWidget(rButton);

        QPushButton *updateButton = new QPushButton();
        updateButton->setText("Update");
        updateButton->setFixedWidth(TASKBUTTON_W);
        updateButton->setStyleSheet("QPushButton {border-style: outset; border-width: 2px; background-color: grey; color: white;} QPushButton:pressed {background-color: white; color: grey}");       
        connect(updateButton, &QPushButton::clicked, this, &TaskBlock::refreshResult);
        line->layout()->addWidget(updateButton);

        result = new QTextBrowser();
        result->setMinimumHeight(TASKWIDGET_H * 1.5);
        result->setMaximumHeight(TASKWIDGET_H * 1.5);
        result->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
        result->setStyleSheet("border-width:0px;");
        this->layout()->addWidget(result);
    }
    if (stdoutput == 0) {
        QWidget *line = this->createLine();

        QLabel *stdoutLabel = new QLabel();
        stdoutLabel->setText("Output :");
        stdoutLabel->setMaximumHeight(TASKWIDGET_H);
        stdoutLabel->setFixedWidth(TASKLABEL_W);
        stdoutLabel->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
        stdoutLabel->setStyleSheet("border-width:0px;");
        line->layout()->addWidget(stdoutLabel);

        stdoutput = new QTextBrowser();
        stdoutput->setMinimumHeight(TASKWIDGET_H * 1.5);
        stdoutput->setMaximumHeight(TASKWIDGET_H * 1.5);
        stdoutput->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
        stdoutput->setStyleSheet("border-width:0px;");
        this->layout()->addWidget(stdoutput);
    }
    if (stderror == 0) {
        QWidget *line = this->createLine();
        QLabel *stderrLabel = new QLabel();
        stderrLabel->setText("Error :");
        stderrLabel->setMaximumHeight(TASKWIDGET_H);
        stderrLabel->setFixedWidth(TASKLABEL_W);
        stderrLabel->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
        stderrLabel->setStyleSheet("border-width:0px;");
        line->layout()->addWidget(stderrLabel);

        stderror = new QTextBrowser();
        stderror->setMinimumHeight(TASKWIDGET_H * 1.5);
        stderror->setMaximumHeight(TASKWIDGET_H * 1.5);
        stderror->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
        stderror->setStyleSheet("border-width:0px;");
        this->layout()->addWidget(stderror);
    }



    return;
}

void TaskBlock::openResult() {
    QProcess *proc = new QProcess(this);
    proc->start("open " + QFileInfo(this->result->source().toString()).absoluteDir().absolutePath());

    return;
}

void TaskBlock::openStdOutput() {
    QProcess *proc = new QProcess(this);
    proc->start("open " + this->stdoutput->source().toString());

    return;
}

void TaskBlock::openStdError() {
    QProcess *proc = new QProcess(this);
    proc->start("open " + this->stderror->source().toString());

    return;
}

 void TaskBlock::executeHand() {
     //qDebug() << "sender: " << sender()->objectName();
     QString handName = sender()->objectName();
     if (handName == "run") {
        if (runCmd.length() > 0) {
            updateResult();
            TaskThread * th = new TaskThread();
            th->cmdline = runCmd;
            th->workpos = mw->talkConfig.running + "/" + mw->talkConfig.startdate + mw->talkConfig.starttime + "." + QString().number(++mw->talkConfig.timelabel);
            //qDebug() << "Task run workpos: " << th->workpos;
            prepareWorkPos(th->workpos);
            th->task = this;
            th->start();
            this->findChild<QPushButton*>("run")->setVisible(false);
            if (redoCmd.length() > 0) {
                this->findChild<QPushButton*>("redo")->setVisible(true);
            }
            if (undoCmd.length() > 0) {
                this->findChild<QPushButton*>("undo")->setVisible(true);
            }
        }
        return;
     }

     if (handName == "redo") {
        if (redoCmd.length() > 0) {
            updateResult();
            TaskThread * th = new TaskThread();
            th->cmdline = redoCmd;
            th->workpos = mw->talkConfig.running + "/" + mw->talkConfig.startdate + mw->talkConfig.starttime + "." + QString().number(++mw->talkConfig.timelabel);
            //qDebug() << "Task redo workpos: " << th->workpos;
            prepareWorkPos(th->workpos);
            th->task = this;
            th->start();
        }
        return;
     }

     if (handName == "undo") {
        if (undoCmd.length() > 0) {
            updateResult();
            TaskThread * th = new TaskThread();
            th->cmdline = undoCmd;
            th->workpos = mw->talkConfig.running + "/" + mw->talkConfig.startdate + mw->talkConfig.starttime + "." + QString().number(++mw->talkConfig.timelabel);
            //qDebug() << "Task undo workpos: " << th->workpos;
            prepareWorkPos(th->workpos);
            th->task = this;
            th->start();
        }
        return;
     }

     if (handName.length() > 0 and cmdEdit != 0) {
        cmdEdit->cmdPush(static_cast<QPushButton *>(sender())->toolTip());
     }

     return;
 }

 void TaskBlock::refreshResult() {
     this->result->reload();
     this->stdoutput->reload();
     this->stderror->reload();
     return;
 }

 void TaskBlock::xmlParseAction(QXmlStreamReader &xml){
    _lastEntryType = "Action";
    if (xml.tokenType() != QXmlStreamReader::StartElement) {
        return;
    }
    xml.readNext();
    while(!(xml.tokenType() == QXmlStreamReader::EndElement and xml.name() == "action")) {
        if (xml.tokenType() == QXmlStreamReader::StartElement) {
            if (xml.name() == "run") {
                xml.readNext();
                runCmd = xml.text().toString().replace("$TALKERONHOME$", mw->talkConfig.home).replace("$HOME$", QDir().homePath());
            }
            if (xml.name() == "redo") {
                xml.readNext();
                redoCmd = xml.text().toString().replace("$TALKERONHOME$", mw->talkConfig.home).replace("$HOME$", QDir().homePath());
            }
            if (xml.name() == "undo") {
                xml.readNext();
                undoCmd = xml.text().toString().replace("$TALKERONHOME$", mw->talkConfig.home).replace("$HOME$", QDir().homePath());
            }
        }
        xml.readNext();
    }
    return;
 }

 void TaskBlock::xmlParsePara(QXmlStreamReader &xml){

    xml.readNext();

    Para para;
    while(!(xml.tokenType() == QXmlStreamReader::EndElement and xml.name() == "para")) {
        if (xml.tokenType() == QXmlStreamReader::StartElement) {
            if (xml.name() == "name") {
                xml.readNext();
                para.name = xml.text().toString();
            }
            if (xml.name() == "type") {
                xml.readNext();
                para.type = xml.text().toString();
            }
            if (xml.name() == "range") {
                xml.readNext();
                para.range = xml.text().toString();
            }
            if (xml.name() == "value") {
                xml.readNext();
                para.value = xml.text().toString().replace("$TALKERONHOME$", mw->talkConfig.home).replace("$HOME$", QDir().homePath());
            }
        }
        xml.readNext();
    }

    if (para.name.length() > 0) {
        if (_lastEntryType != "Para" or _lineAbility < 1) {

            if (_lastEntryType != "Para") {
                QFrame *separator = new QFrame();
                separator->setObjectName(QString::fromUtf8("line"));
                separator->setFrameShape(QFrame::HLine);
                separator->setFrameShadow(QFrame::Sunken);
                this->layout()->addWidget(separator);
            }
            _lastEntryType = "Para";
            _currentLine = createLine();
            _lineAbility = 3;

        }
        QLabel *paraLabel = new QLabel();
        paraLabel->setText(para.name);
        paraLabel->setMaximumHeight(TASKWIDGET_H);
        paraLabel->setFixedWidth(TASKLABEL_W);
        paraLabel->setAlignment(Qt::AlignCenter);
        _currentLine->layout()->addWidget(paraLabel);
        QLineEdit *paraEdit = new QLineEdit();
        paraEdit->setText(para.value);
        paraEdit->setObjectName(para.name);
        paraEdit->setMaximumHeight(TASKWIDGET_H);
        paraEdit->setFixedWidth(TASKFIELD_W);
        paraEdit->setAlignment(Qt::AlignCenter);
        paraEdit->setStyleSheet("border-style: outset; border-width: 1px;");
        paraNames << para.name;
        _currentLine->layout()->addWidget(paraEdit);

        _lineAbility -= 1;
    }

    return;
 }

 void TaskBlock::xmlParseHand(QXmlStreamReader &xml){

     QString alias = xml.attributes().value("alias").toString();
     xml.readNext();
     if (xml.text().toString().length() > 0) {
         if (_lastEntryType != "Hand" or _lineAbility < 1) {

            if (_lastEntryType != "Hand") {
                QFrame *separator = new QFrame();
                separator->setObjectName(QString::fromUtf8("line"));
                separator->setFrameShape(QFrame::HLine);
                separator->setFrameShadow(QFrame::Sunken);
                this->layout()->addWidget(separator);
            }
            _lastEntryType = "Hand";
            _currentLine = createLine();
            _lineAbility = 5;
         }
         QPushButton *handButton = new QPushButton();

         if (alias.length() > 0) {
            handButton->setText(alias);
         } else {
            handButton->setText(xml.text().toString().split(" ")[0].split(".").last());
         }
         handButton->setObjectName(xml.text().toString().split(" ")[0]);
         handButton->setToolTip(xml.text().toString().replace("$TALKERONHOME$", mw->talkConfig.home).replace("$HOME$", QDir().homePath()));
         handButton->setFixedWidth(TASKBUTTON_W);
         handButton->setStyleSheet("QPushButton {border-style: outset; border-width: 2px; background-color: grey; color: white;} QPushButton:pressed {background-color: white; color: grey}");
         connect(handButton, &QPushButton::clicked, this, &TaskBlock::executeHand);
         _currentLine->layout()->addWidget(handButton);

         _lineAbility -= 1;
     }
 }

 void TaskBlock::openAssistFolder() {
     QProcess *proc = new QProcess(this);
     proc->start("open " + QFileInfo(assistXmlPath).absoluteDir().absolutePath());

     return;
 }

 void TaskBlock::prepareWorkPos(QString workPos) {

     if (! QDir().exists(workPos)) {
         QDir().mkdir(workPos);
     }

     QString resultFilePath = workPos + "/result.txt";
     if (! QFile().exists(resultFilePath)) {
         QFile resultFile(resultFilePath);
         if (!resultFile.open(QIODevice::WriteOnly | QIODevice::Text)) {
             //qDebug() << "Create result file: " << resultFilePath;
             return;
         }
         resultFile.write(("# result for running execution " + workPos.split("/").last() +"\n").toLocal8Bit());
         resultFile.close();
     }

     QString outputFilePath = workPos + "/output.txt";
     if (! QFile().exists(outputFilePath)) {
         QFile outputFile(outputFilePath);
         if (!outputFile.open(QIODevice::WriteOnly | QIODevice::Text)) {
             //qDebug() << "Create output file: " << outputFilePath;
             return;
         }
         outputFile.write(("# output for running execution " + workPos.split("/").last() + "\n").toLocal8Bit());
         outputFile.close();
     }

     QString errorFilePath = workPos + "/error.txt";
     if (! QFile().exists(errorFilePath)) {
         QFile errorFile(errorFilePath);
         if (!errorFile.open(QIODevice::WriteOnly | QIODevice::Text)) {
             //qDebug() << "Create error file: " << errorFilePath;
             return;
         }
         errorFile.write(("# error for running execution " + workPos.split("/").last() + "\n").toLocal8Bit());
         errorFile.close();
     }

     QString inputFilePath = workPos + "/input.txt";
     if (! QFile().exists(inputFilePath)) {
         QFile inputFile(inputFilePath);
         if (!inputFile.open(QIODevice::WriteOnly | QIODevice::Text)) {
             //qDebug() << "Create input file: " << inputFilePath;
             return;
         }
         for (int i = 0; i < paraNames.length(); i++) {
             inputFile.write((paraNames[i] + "\t" + this->findChild<QLineEdit *>(paraNames[i])->text() + "\n").toLocal8Bit());
         }
         inputFile.close();
     }

     this->result->setSource(QUrl(resultFilePath));
     this->stdoutput->setSource(QUrl(outputFilePath));
     this->stderror->setSource(QUrl(errorFilePath));

     return;
 }


