#include <iostream>
#include <string>
#include "commandlinemanager.h"
#include "methodresolver.h"
#include "pathmanager.h"
#include "measurer.h"

using namespace std;


int main( int argc, char** argv ) {

    CommandLineManager parser( argc, argv );

    if( parser.isInputValid() ) {

        string method = parser.getMethod();
        string referencePath = parser.getReferencePath();
        string dataPath = parser.getDataPath();
        int usersNumber = parser.getUsersNumber();
        float epsilon = parser.getEpsilon();
        int frames = parser.getFramesNumber();
        bool printVerbose = parser.isPrintVerbose();

        MethodResolver resolver;

        if( method == "bhi" ) {
            // Our evaluation method.

            int distance = parser.getDistance();
            bool doubleZone = parser.isDoubleEnabled();

            resolver.evaluateBHI( epsilon, distance, referencePath, dataPath, doubleZone, usersNumber, frames, printVerbose );
        } else if( method == "cus" ) {
            // CUS evaluation method.

            resolver.evaluateCUS( epsilon, referencePath, dataPath, usersNumber, frames, printVerbose );
        }

        resolver.printResults();
    }
    else {
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
