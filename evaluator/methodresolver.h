#ifndef METHODRESOLVER_H
#define METHODRESOLVER_H

#include <iostream>
#include <getopt.h>
#include <stdlib.h>
#include "commandlinemanager.h"
#include "pathmanager.h"

using namespace std;

class MethodResolver
{
public:
    void evaluateBHI(float epsilon, int distance, string referencePath, string dataPath, bool doubleZone, int usersNumber, int frames, bool printVerbose);
    void evaluateCUS(float epsilon, string referencePath, string dataPath, int usersNumber, int frames, bool printVerbose);
    void printResults();

private:
    void evaluate(float epsilon, int distance, string referencePath, string dataPath, bool doubleZone, int usersNumber, int frames, bool printVerbose);
    float CUSa;
    float CUSe;
    float precision;
    float recall;
    float Kappa;
    double Fmeasure;
    bool printVerbose;
};

#endif // METHODRESOLVER_H
