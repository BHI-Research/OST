#ifndef MEASURER_H
#define MEASURER_H

#include <iostream>
#include <vector>
#include <math.h>
#include "frame.h"

using namespace std;

class Measurer
{
public:
    Measurer(int windowFrames, double distanceThreshold, bool useDoubleWindow);
    virtual ~Measurer();

    void computeMetrics();
    void printResults();
    bool isStillComputing();

    void setReferenceData(vector<Frame> data);
    void setMeasuredData(vector<Frame> data);

    void setTotalFrameNumber(int total);

    double getCUSa();
    double getCUSe();
    double getFmeasure();
    double getKappa();

private:
    int windowFrames;
    bool useDoubleSide, isComputing;
    double distanceThreshold, kappa;
    string referencePath, dataPath;
    vector<Frame> referenceData;
    vector<Frame> meassuredData;
    int numberFramesMatched, numberFramesNonMatched, numberFramesReference, numerFramesMeasure, totalNumberOfFrames;

};

#endif // MEASURER_H
