#include "frame.h"

Frame::Frame(int number, Mat frame) {

    this->number = number;
    this->frame = frame;
}

Frame::~Frame() {
}

double Frame::comparHistogramTo( Frame anotherFrame ) {

    double frameDistance = -1.0f;

    /// Convert to HSV
    Mat hsvThisFrame, hsvAnotherFrame;
    cvtColor( this->frame, hsvThisFrame, COLOR_BGR2HSV );
    cvtColor( anotherFrame.getFrameMat(), hsvAnotherFrame, COLOR_BGR2HSV );

    /// Using 50 bins for hue and 60 for saturation
    int h_bins = 50; int s_bins = 60;
    int histSize[] = { h_bins, s_bins };

    // hue varies from 0 to 179, saturation from 0 to 255
    float h_ranges[] = { 0, 180 };
    float s_ranges[] = { 0, 256 };

    const float* ranges[] = { h_ranges, s_ranges };

    // Use the o-th and 1-st channels
    int channels[] = { 0, 1 };


    /// Histograms
    MatND histogramThisFrame;
    MatND histogramAnotherFrame;

    /// Calculate the histograms for the HSV images
    calcHist( &hsvThisFrame, 1, channels, Mat(), histogramThisFrame, 2, histSize, ranges, true, false );
    normalize( histogramThisFrame, histogramThisFrame, 0, 1, NORM_MINMAX, -1, Mat() );

    calcHist( &hsvAnotherFrame, 1, channels, Mat(), histogramAnotherFrame, 2, histSize, ranges, true, false );
    normalize( histogramAnotherFrame, histogramAnotherFrame, 0, 1, NORM_MINMAX, -1, Mat() );

    /// Apply the histogram comparison method
    frameDistance = compareHist( histogramThisFrame, histogramAnotherFrame, METHOD_COMPARE_CORRELATION );

    return frameDistance;
}

Mat Frame::getFrameMat() {
    return this->frame;
}

int Frame::getPosition() {
    return this->number;
}
