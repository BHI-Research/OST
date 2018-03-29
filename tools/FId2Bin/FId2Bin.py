#!/usr/bin/env python

import pandas as panda
import cv2
import os
import csv
import numpy as np
import argparse

#/*********************************************************************************************    

def get_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('video',   type=str, help='video name with extension')
    parser.add_argument('input_file',   type=str, help='input csv file')
    parser.add_argument('output_file',   type=str, help='output csv file')
    args = vars(parser.parse_args())

    return args['video'],args['input_file'],args['output_file']

#/*********************************************************************************************    

def csv_to_matrix(file):
    file= file + '.csv'
    output = list(csv.reader(open(file, "rb"), delimiter=","))
    return output[0]

#/*********************************************************************************************    

def matrix_to_csv(file, matrix):
    file = file +'.csv'
    df=panda.DataFrame(matrix)
    df.to_csv(file, sep=',', encoding='utf-8', index=False,header=False)

#/*********************************************************************************************    

def get_video_info(video_name):

    cap = cv2.VideoCapture(video_name)

    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    ret, frame = cap.read()

    if frame is None:
        print 'ERROR: VIDEO NOT FOUND'
        return
    elif length == 0:
        print 'ERROR: VIDEO NOT FOUND'
        return

    cap.release()
    return length

#/*********************************************************************************************    

def IDs_to_bin_csv(lenght, file_input_csv, file_output_csv):
    frames_input=csv_to_matrix(file_input_csv)
    rows = len(frames_input)
    frames_output=np.zeros(shape=(1,lenght),dtype=int)

    for j in range ( 0, rows):
        index= int(frames_input[j])
        frames_output[0][index]=1

    matrix_to_csv(file_output_csv, frames_output)

#************************************************************************************************************

if __name__ == '__main__':

    video_file, input_csv,output_csv = get_args()

    #CSV WITH FRAMES ID's TO CSV WITH 0 & 1

    length =  get_video_info(video_file)
    IDs_to_bin_csv(length, input_csv, output_csv)
