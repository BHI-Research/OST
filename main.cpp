#include <iostream>
#include <string>
#include "commandlinemanager.h"
#include "pathmanager.h"
#include "measurer.h"

using namespace std;

void printResults( float CUSa, float CUSe, float Fmeter, float Kappa, bool printVerbose ) {

    if( printVerbose ) {
        cout << "CUSa: " << CUSa << endl;
        cout << "CUSe: " << CUSe << endl;
        cout << "F-meter: " << Fmeter << endl;
        cout << "Cohen's Kappa: " << Kappa << endl;
    }
    else {
        cout << CUSa << "\t" << CUSe << "\t" << Fmeter << "\t" << Kappa;
    }

}

int main( int argc, char** argv ) {

    CommandLineManager parser( argc, argv );

    if( parser.isInputValid() ) {

        string referencePath = parser.getReferencePath();
        string dataPath = parser.getDataPath();

        PathManager dataPathManager( dataPath );

        int usersNumber = parser.getUsersNumber();
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

                Measurer measurer( parser.getDistance(),
                                   parser.getEpsilon(),
                                   parser.isDoubleEnabled() );
                measurer.setReferenceData( referencePathManager.getFrameList() );
                measurer.setMeasuredData( dataPathManager.getFrameList() );
                measurer.setTotalFrameNumber( parser.getFramesNumber() );

                measurer.computeMetrics();

                CUSa = CUSa + measurer.getCUSa();
                CUSe = CUSe + measurer.getCUSe();
                Kappa = Kappa + measurer.getKappa();
            }
            else {
                cout << "Path is not valid." << endl;
            }
        }

        CUSa = CUSa / (double)parser.getUsersNumber();
        CUSe = CUSe / (double)parser.getUsersNumber();
        Kappa = Kappa / (double)parser.getUsersNumber();

        double recall = CUSa;
        double precision = CUSa / ( CUSa + CUSe );

        double Fmeter = ( 2.0 * precision * recall ) / ( precision + recall );

        bool printVerbose = parser.isPrintVerbose();
        printResults(CUSa, CUSe, Fmeter, Kappa, printVerbose);
    }
    else {
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
