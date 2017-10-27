#ifndef FRAME_H
#define FRAME_H

#include "opencv2/imgproc/imgproc.hpp"

using namespace cv;

class Frame
{
public:
    static const int METHOD_COMPARE_CORRELATION = 0;

    Frame(int number, Mat frame);
    virtual ~Frame();

    double comparHistogramTo(Frame anotherFrame);
    Mat getFrameMat();
    int getPosition();

private:
    int number;
    Mat frame;
};

#endif // FRAME_H
