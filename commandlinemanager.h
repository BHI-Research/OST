#ifndef COMMANDLINEMANAGER_H
#define COMMANDLINEMANAGER_H

#include <iostream>
#include <getopt.h>
#include <stdlib.h>

using namespace std;

class CommandLineManager
{
public:
    CommandLineManager(int argc, char** argv);

    float getEpsilon();
    int getDistance();
    int getUsersNumber();
    int getFramesNumber();
    string getReferencePath();
    string getDataPath();
    string getMethod();
    bool isDoubleEnabled();
    bool isPrintVerbose();

    bool isInputValid();

private:
    bool validInput;
    bool doubleZoneIsEnable;
    bool printVerboseEnable;
    float epsilon;
    int distance;
    int users;
    int frames;
    string referencePath;
    string dataPath;
    string method;
};

#endif // COMMANDLINEMANAGER_H
