#ifndef PATHMANAGER_H
#define PATHMANAGER_H

#include <dirent.h>
#include <iostream>
#include <stdlib.h>
#include <opencv2/highgui/highgui.hpp>
#include "frame.h"

using namespace std;

class PathManager
{
public:
    PathManager(string dirPath);
    virtual ~PathManager();

    bool isPathValid();
    vector<Frame> getFrameList();
    void showAllImagesInVector();

private:    
    void showImage(Mat image, int number);
    int getNumberFromString(string inputString);
    bool isValid;
    vector<Frame> frameList;
    string directoryPath;
};

#endif // PATHMANAGER_H
