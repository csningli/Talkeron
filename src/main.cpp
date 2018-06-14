#include "mainwindow.h"
#include <QApplication>

MainWindow *mw;

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    mw = new MainWindow();
    mw->show();

    return a.exec();
}
