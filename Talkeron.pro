#-------------------------------------------------
#
# Project created by QtCreator 2016-09-29T11:19:59
#
#-------------------------------------------------

QT       += core gui xml

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = Talkeron
TEMPLATE = app

INCLUDEPATH += src/
#QMAKE_MAC_SDK = macosx10.12


SOURCES += src/cmdcompileresult.cpp \
    src/cmdtextedit.cpp \
    src/main.cpp \
    src/mainwindow.cpp \
    src/taskblock.cpp \
    src/taskscrollarea.cpp \
    src/taskthread.cpp

HEADERS  += src/cmdcompileresult.h \
    src/cmdtextedit.h \
    src/mainwindow.h \
    src/talkerxml.h \
    src/taskblock.h \
    src/taskscrollarea.h \
    src/taskthread.h

FORMS    += mainwindow.ui

ICON = appicon.icns

CONFIG += c++11

DISTFILES += \
    createicons.src \
    TalkeronAssist/Talkeron.talk

mac {
        DEFINES += UNIX MACOSX
        QMAKE_POST_LINK += $$PWD/link_to_applications.sh
        QMAKE_MACOSX_DEPLOYMENT_TARGET = 10.7
}
