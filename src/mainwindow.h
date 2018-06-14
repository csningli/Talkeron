#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "taskblock.h"
#include "cmdcompileresult.h"


namespace Ui {
    class MainWindow;
    class CmdTextEdit;
    class TaskBlock;
}

struct TalkeronConfig
{
    QString home;
    QString assists;
    QString actions;
    QString running;
    QString history;
    QString startdate;
    QString starttime;
    int timelabel;
};

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();
    TalkeronConfig talkConfig;

protected :
    void closeEvent(QCloseEvent *event);

private slots:
    void handleCmdInput();
    CmdCompileResult *compileCmd(QString cmd);
    void createTask(QString cmd);
    void areaChanged(int, int);

private:
    Ui::MainWindow *ui;
    void init();

};



#endif // MAINWINDOW_H
