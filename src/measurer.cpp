#include "measurer.h"

Measurer::Measurer( int windowFrames, double distance, bool useDoubleWindow ) {

    this->windowFrames = windowFrames;
    this->distanceThreshold = distance;
    this->useDoubleSide = useDoubleWindow;
    this->isComputing = false;
    this->referenceData.clear();
    this->meassuredData.clear();
    this->totalNumberOfFrames = 0;
}

Measurer::~Measurer() {

    referenceData.clear();
    meassuredData.clear();
}

void Measurer::setTotalFrameNumber( int total ) {

    this->totalNumberOfFrames = total;
}

void Measurer::computeMetrics() {

    this->isComputing = true;
    int firstWindowFrame = 0, lastWindowFrame = 0;
    double actualDistance = 0.0f;

    //reset values
    numberFramesMatched = 0;
    numberFramesNonMatched = 0;
    numberFramesReference = referenceData.size();
    numberFramesMeasure = meassuredData.size();

    // Duplicate meassureData to avoid wrong results.
    vector<Frame> newMeassuredData = meassuredData;

    for( vector<Frame>::iterator itR = referenceData.begin(); itR != referenceData.end(); itR++ ) {

        for( vector<Frame>::iterator itM = newMeassuredData.begin(); itM != newMeassuredData.end(); itM++ ) {

            //update frames to compare
            Frame measuredFrame = (Frame) *itM;
            Frame referenceFrame = (Frame) *itR;

            //check frame distance
            if( useDoubleSide ) {
                firstWindowFrame = referenceFrame.getPosition() - windowFrames;
            }
            else {
                firstWindowFrame = referenceFrame.getPosition();
            }

            lastWindowFrame = referenceFrame.getPosition() + windowFrames;

            //check delta distance
            if( windowFrames < 0 || (measuredFrame.getPosition() >= firstWindowFrame ) &&
                (measuredFrame.getPosition() <= lastWindowFrame) ) {
                actualDistance = referenceFrame.comparHistogramTo( measuredFrame );
                if( fabs(actualDistance) > this->distanceThreshold ) {
                    numberFramesMatched++;
                    //cout << "matched refence " << referenceFrame.getPosition() <<
                    //        " and measured " << measuredFrame.getPosition() <<
                    //        " distance: " << actualDistance << endl;

                    // If the frame is matched, remove it from vector.
                    newMeassuredData.erase(itM);
                    break;
                }
            }
        }
    }
    // cout << "meassured data: " << meassuredData.size() << endl;
    // cout << "number frames matched: " << numberFramesMatched << endl;
    numberFramesNonMatched = meassuredData.size() - numberFramesMatched;
    this->isComputing = false;
    // this->printResults();
}

bool Measurer::isStillComputing() {
    return this->isComputing;
}

void Measurer::setReferenceData( vector<Frame> data ) {
    this->referenceData = data;
}

void Measurer::setMeasuredData( vector<Frame> data ) {
    this->meassuredData = data;
}

double Measurer::getPrecision() {
    double result = 0.0f;
    if( 0 != numberFramesMeasure ) {
        result = (double)numberFramesMatched / (double)numberFramesMeasure;
    }
    else {
        result = -1.0f;
    }

    return result;
}

double Measurer::getRecall() {
    double result = 0.0f;
    if( 0 != numberFramesReference ) {
        result = (double)numberFramesMatched / (double)numberFramesReference;
    }
    else {
        result = -1.0f;
    }

    return result;
}

double Measurer::getCUSa() {

    double result = 0.0f;
    if( 0 != numberFramesReference ) {
        result = (double)numberFramesMatched / (double)numberFramesReference;
    }
    else {
        result = -1.0f;
    }

    return result;
}

double Measurer::getCUSe() {
    double result = 0.0f;
    if( 0 != numberFramesReference ) {
        result = (double)numberFramesNonMatched / (double)numberFramesReference;
    }
    else {
        result = -1.0f;
    }

    return result;
}

double Measurer::getFmeasure() {
    double recall = getRecall();
    double precision = getPrecision();

    if( !recall && !precision ) {
        return -1.0f;
    }

    double Fmeter = ( 2.0 * precision * recall ) / ( precision + recall );

    return Fmeter;
}

double Measurer::getKappa() {
    double pO, pE, pEn, pEy, kappa;

    int nYmYr, nNmNr, nNmYr, nYmNr;

    nYmYr = numberFramesMatched;
    nNmYr = numberFramesReference - numberFramesMatched;
    nYmNr = numberFramesMeasure - numberFramesMatched;
    nNmNr = totalNumberOfFrames - nYmYr - nNmYr - nYmNr;

    pO = (double)( nYmYr + nNmNr ) / (double)totalNumberOfFrames;

    pEn = ( (double)( nNmNr + nNmYr ) / (double)totalNumberOfFrames ) *
            ( (double)( nNmNr + nYmNr ) / (double)totalNumberOfFrames );
    pEy = ( (double)( nYmYr + nYmNr ) / (double)totalNumberOfFrames ) *
            ( (double)( nYmYr + nNmYr ) / (double)totalNumberOfFrames );
    pE = pEn + pEy;

    kappa = (pO - pE) / (1 - pE);

    return kappa;
}

void Measurer::printResults() {
    cout << "CUSa: " << this->getCUSa() << endl;
    cout << "CUSe: " << this->getCUSe() << endl;
    cout << "F-meter: " << this->getFmeasure() << endl;
    cout << "Cohen's Kappa: " << this->getKappa() << endl;
    cout << "numberFramesMatched: " << numberFramesMatched << endl;
    cout << "numberFramesNonMatched: " << numberFramesNonMatched << endl;
    cout << "numberFramesReference: " << numberFramesReference << endl;
}
