#include "methodresolver.h"
#include "measurer.h"
#include <stdio.h>
#include <stdlib.h>

using namespace std;

void MethodResolver::evaluateBHI(float epsilon, int distance, string referencePath, string dataPath, bool doubleZone, int usersNumber, int frames, bool printVerbose) {
    evaluate(epsilon, distance, referencePath, dataPath, doubleZone, usersNumber,frames, printVerbose);
}

void MethodResolver::evaluateCUS(float epsilon, string referencePath, string dataPath, int usersNumber, int frames, bool printVerbose) {
    // Disable distance
    int distance = -1;
    bool doubleZone = true;

    evaluate(epsilon, distance, referencePath, dataPath, doubleZone, usersNumber,frames, printVerbose);
}

void MethodResolver::evaluate(float epsilon, int distance, string referencePath, string dataPath, bool doubleZone, int usersNumber, int frames, bool printVerbose) {

    PathManager dataPathManager( dataPath );

    float CUSa = 0.0f;
    float CUSe = 0.0f;
    float Kappa = 0.0f;

    for( int i = 1; i <= usersNumber; i++ ) {

        // Convert int to string
        // to_string(int) does not work
        string userString = static_cast<ostringstream*>( &(ostringstream() << i) )->str();

        string currentPath = referencePath + "/" + "user" + userString + "/";
        PathManager referencePathManager(currentPath);

        if( referencePathManager.isPathValid() && dataPathManager.isPathValid() ) {

            Measurer measurer( distance,
                    epsilon,
                    doubleZone );
            measurer.setReferenceData( referencePathManager.getFrameList() );
            measurer.setMeasuredData( dataPathManager.getFrameList() );
            measurer.setTotalFrameNumber( frames );

            measurer.computeMetrics();

            CUSa = CUSa + measurer.getCUSa();
            CUSe = CUSe + measurer.getCUSe();
            Kappa = Kappa + measurer.getKappa();
        }
        else {
            cout << "Path is not valid." << endl;
        }
    }

    CUSa = CUSa / (double)usersNumber;
    CUSe = CUSe / (double)usersNumber;
    Kappa = Kappa / (double)usersNumber;

    double recall = CUSa;
    double precision = CUSa / ( CUSa + CUSe );

    double Fmeter = ( 2.0 * precision * recall ) / ( precision + recall );

    this->CUSa = CUSa;
    this->CUSe = CUSe;
    this->Kappa = Kappa;
    this->Fmeter = Fmeter;
    this->printVerbose = printVerbose;
}

void MethodResolver::printResults() {
    if( printVerbose ) {
        cout << "CUSa: " << this->CUSa << endl;
        cout << "CUSe: " << this->CUSe << endl;
        cout << "F-meter: " << this->Fmeter << endl;
        cout << "Cohen's Kappa: " << this->Kappa << endl;
    }
    else {
        cout << this->CUSa << "\t" << this->CUSe << "\t" << this->Fmeter << "\t" << this->Kappa;
    }

}
