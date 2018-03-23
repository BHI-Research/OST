'''
Superframe to Keyframe converter.

Given a CSV file as input, where each row represents an user and a sequence of 1's represents a supeframe,
produces a new CSV file where superframes are converted into keyframes.

Example of use:

python superframe-to-keyframe.py --input input.csv --output output.csv --frame first
'''

from csv import reader, writer
from random import randint
import numpy as np
import argparse
import math


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', type=str, required=True,
                        help='The CSV input file')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help='The CSV output file')
    parser.add_argument('-f', '--frame', choices=['first', 'middle', 'last', 'random'], required=True,
                        help='Which frame of the interval we want to choose as keyframe')
    args = vars(parser.parse_args())

    return args['input'], args['output'], args['frame']


def get_superframes_intervals(data):
    array = []
    onSuperframe = False

    for index, stringNumber in enumerate(data):
        number = int(stringNumber)
        if number != 0 and not onSuperframe:
            # Superframe starts
            array.append(index)
            onSuperframe = True
        elif number == 0 and onSuperframe:
            # Superframe ends
            array.append(index-1)
            onSuperframe = False
        elif number != 0 and index == len(data) - 1:
            # Superframe ends
            array.append(index)

    return array


def convert_to_keyframes(intervals, length, frame):
    array = np.zeros((length,), dtype=np.int)
    if frame == 'first':
        justEven = intervals[::2]
        for index in justEven:
            array[index] = 1
    elif frame == 'last':
        justOdd = intervals[1::2]
        for index in justOdd:
            array[index] = 1
    elif frame == 'middle':
        npIntervals = np.asarray(intervals)
        howMany = len(intervals)/2
        splitIntervals = np.array_split(npIntervals, howMany)
        for interval in splitIntervals:
            middle = int(math.floor((interval[1] - interval[0])/2) + interval[0])
            array[middle] = 1
    elif frame == 'random':
        npIntervals = np.asarray(intervals)
        howMany = len(intervals)/2
        splitIntervals = np.split(npIntervals, howMany)
        for interval in splitIntervals:
            random = randint(interval[0], interval[1])
            array[random] = 1

    return array


if __name__ == '__main__':
    inputFile, outputFile, frame = get_args()
    csvFile = open(inputFile, 'rb')
    data = reader(csvFile)

    with open(outputFile, 'wb') as csvfile:
        spamwriter = writer(csvfile)
        for row in data:
            superframesInterval = get_superframes_intervals(row)
            keyframe = convert_to_keyframes(superframesInterval, len(row), frame)
            spamwriter.writerow(keyframe)
