#include "pathmanager.h"

PathManager::PathManager( string dirPath ) {

    DIR *dir;
    this->directoryPath = dirPath;

    const char *dirPathChar = dirPath.c_str();
    if( ( dir = opendir( dirPathChar ) ) != NULL ) {
        struct dirent *ent;

        dirPath = dirPath + "/";

        frameList.clear();

        while( ( ent = readdir( dir ) ) != NULL ) {


            if( (string)ent->d_name != "." && (string)ent->d_name != ".." && getNumberFromString( (string)ent->d_name) >= 0 ) {
                Mat matImage = imread( dirPath + (string)ent->d_name, IMREAD_COLOR );

                Frame image( getNumberFromString( (string)ent->d_name ), matImage );
                frameList.push_back( image );
            }
        }
        closedir( dir );
        isValid = true;
    }
    else {
        isValid = false;
    }
}

PathManager::~PathManager() {
    frameList.clear();
}

void PathManager::showImage( Mat image, int number ) {
    if(! image.data ) {
        cout <<  "Could not open or find the image" << std::endl ;
    }
    else {
        stringstream ss;
        ss << number;
        string windowTitle = this->directoryPath + " " + ss.str();
        namedWindow( windowTitle, WINDOW_AUTOSIZE );
        imshow( windowTitle, image );
        waitKey(0);
    }
}

int PathManager::getNumberFromString( string inputString ) {
    string temp;
    int number=0;

    for( unsigned int i = 0; i < inputString.size(); i++ ) {
        if( isdigit( inputString[i] ) ) {
            for( unsigned int a = i; a < inputString.size(); a++ ) {
                temp += inputString[a];
            }
            break;
        }
    }

    istringstream resultStream(temp);
    resultStream >> number;

    return number;
}

void PathManager::showAllImagesInVector() {
    for( vector<Frame>::iterator it = frameList.begin(); it != frameList.end(); it++ ) {
        Frame aFrame = (Frame) *it;
        this->showImage( aFrame.getFrameMat(), aFrame.getPosition() );
    }
}

bool PathManager::isPathValid() {
    return this->isValid;
}

vector<Frame> PathManager::getFrameList() {
    return this->frameList;
}
