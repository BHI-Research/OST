cmake_minimum_required(VERSION 2.8)
project( evaluator )
find_package( OpenCV REQUIRED )
add_executable( evaluator commandlinemanager.h frame.h measurer.h pathmanager.h methodresolver.h commandlinemanager.cpp
           frame.cpp
           main.cpp
           measurer.cpp
           pathmanager.cpp
           methodresolver.cpp )
target_link_libraries( evaluator ${OpenCV_LIBS} )
