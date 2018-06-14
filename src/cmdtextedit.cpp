#include "cmdtextedit.h"
#include<QKeyEvent>
#include<QTextCursor>
#include<QDebug>


CmdTextEdit::CmdTextEdit(QWidget *parent)
{
    //QTextEdit(parent);
    setFontWeight(12);
}

void CmdTextEdit::keyPressEvent(QKeyEvent *event)
{
    if (event->key() == Qt::Key_Return) {
        emit enterPressed();
    } else if (event->key() == Qt::Key_Up) {
        if (cmdMemoryIndex > cmdMemory.length()) {
            addMemory();
        }
        cmdMemoryIndex -= 1;
        if (cmdMemoryIndex < 0) cmdMemoryIndex = 0;
        if (cmdMemoryIndex < cmdMemory.length()) {
            this->setText(cmdMemory[cmdMemoryIndex]);
        }
        this->moveCursor(this->textCursor().End);
    } else if (event->key() == Qt::Key_Down) {
        if (cmdMemoryIndex < cmdMemory.length() - 1) {
            cmdMemoryIndex += 1;
            this->setText(cmdMemory[cmdMemoryIndex]);
            this->moveCursor(this->textCursor().End);
        }
    } else {
        QTextEdit::keyPressEvent(event);
    }

    //qDebug() << "cmdMemory length: " << cmdMemory.length();
    //qDebug() << "cmdMemoryIndex: " << cmdMemoryIndex;
}

void CmdTextEdit::cmdPush(QString cmd) {
    this->setText(cmd);
    emit enterPressed();
}

void CmdTextEdit::addMemory() {
    if (this-toPlainText().length() > 0) {
        cmdMemory << this->toPlainText();
        cmdMemoryIndex = cmdMemory.length();
        this->setText("");
    }
}

void CmdTextEdit::saveMemory(QString filename) {
    QFile file(filename);
    if (file.open(QIODevice::WriteOnly)) {
        QDataStream out(&file);
        out.setVersion(QDataStream::Qt_5_7);
        out << cmdMemory;
    }
}

void CmdTextEdit::loadMemory(QString filename) {
    QFile file(filename);
    if (file.open(QIODevice::ReadOnly)) {
        QDataStream in(&file);
        in.setVersion(QDataStream::Qt_5_7);
        cmdMemory.clear();   // clear existing contacts
        in >> cmdMemory;
        while (cmdMemory.length() > 10) {
            cmdMemory.pop_front();
        }
        cmdMemoryIndex = cmdMemory.length();
    }
}

