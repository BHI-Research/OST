######################################################################
# Automatically generated by qmake (2.01a) Tue Jul 15 18:51:22 2014
######################################################################

TEMPLATE = app
TARGET = metric
DEPENDPATH += .
INCLUDEPATH += . `pkg-config opencv --cflags`
LIBS += `pkg-config opencv --libs`

# Input
HEADERS += commandlinemanager.h frame.h measurer.h pathmanager.h
SOURCES += commandlinemanager.cpp \
           frame.cpp \
           main.cpp \
           measurer.cpp \
           pathmanager.cpp