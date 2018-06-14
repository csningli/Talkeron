#ifndef CMDTEXTEDIT_H
#define CMDTEXTEDIT_H

#include<QTextEdit>
#include<QStringList>

class CmdTextEdit : public QTextEdit
{
    Q_OBJECT

public :
    CmdTextEdit(QWidget *parent);
    void keyPressEvent(QKeyEvent *event);
    void cmdPush(QString cmd);
    void addMemory();
    void saveMemory(QString filename);
    void loadMemory(QString filename);
    QStringList cmdMemory;
    int cmdMemoryIndex = 0;

signals :
    void enterPressed();
};



#endif // CMDTEXTEDIT_H
