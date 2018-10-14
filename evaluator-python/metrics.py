import cv2
import os
import numpy as np
import shutil
import glob
import ntpath
import re

AUTOMATIC_SUMMARY_FRAMES_PATH   = 'data/data'
USER_SUMMARIES_FRAMES_BASE_PATH = 'data/reference'


def computeMetricsFromArrays(
        user_summary,
        machine_summary,
        video,
        epsilon,
        metric,
        distance,
        aSummaryFramesPath=AUTOMATIC_SUMMARY_FRAMES_PATH,
        uSummaryFramesPath=USER_SUMMARIES_FRAMES_BASE_PATH):
    prepare_folders(user_summary, machine_summary, video)
    cap = cv2.VideoCapture(video)
    videoLength = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if metric == 'cus':
        f1, kappa = computeCUS(
            epsilon,
            videoLength,
            uSummaryFramesPath,
            aSummaryFramesPath,
        )
    else:
        f1, kappa = computeBHI(
            epsilon,
            videoLength,
            distance,
            USER_SUMMARIES_FRAMES_BASE_PATH,
            AUTOMATIC_SUMMARY_FRAMES_PATH
        )

    return f1, kappa


def prepare_folders(uSummary, aSummary, video,
                    aSummaryFramesPath=AUTOMATIC_SUMMARY_FRAMES_PATH,
                    uSummaryFramesPath=USER_SUMMARIES_FRAMES_BASE_PATH):
    vidcap = cv2.VideoCapture(video)
    total_summ_frames = len(aSummary)
    total_video_frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)

    print('Total video frames', total_video_frames)
    print('Total summ frames', total_summ_frames)

    if total_video_frames != total_summ_frames:
        print("Frames don't match")

    if os.path.exists('data'):
        shutil.rmtree('data')

    os.makedirs(aSummaryFramesPath)
    os.makedirs(uSummaryFramesPath)

    aSelectedFrames = np.where(aSummary == 1.0)
    print('Genereting frames from automatic summary')
    for frame_id in aSelectedFrames[0]:
        print('writing frame', frame_id)
        vidcap.set(1,frame_id);
        ret, frame = vidcap.read()
        frame_name = aSummaryFramesPath + '/frame' + str(frame_id) + '.jpg'
        cv2.imwrite(frame_name, frame)

    print('Genereting frames from user summaries. Total number of users: ', len(uSummary))
    for index, user in enumerate(uSummary):
        print('User' + str(index+1) + '...')
        os.makedirs(uSummaryFramesPath + '/user' + str(index+1))
        userFrames = np.where(user == 1.0)

        for frame_id in userFrames[0]:
            print('writing frame', frame_id)
            vidcap.set(1, frame_id);
            ret, frame = vidcap.read()
            frame_name = uSummaryFramesPath + '/user' + str(index+1) + '/frame' + str(frame_id).zfill(4) + '.jpg'
            cv2.imwrite(frame_name, frame)


def computeMetrics(userFolder, predictionImages, refPath, epsilon, videoFrames, distance):
    h_bins = 50
    s_bins = 60
    histSize = [h_bins, s_bins]
    h_ranges = [0, 180]
    s_ranges = [0, 256]
    ranges = h_ranges + s_ranges # concat lists
    channels = [0, 1]

    usrImages = sorted(glob.glob(refPath + '/' + userFolder + '/*.*'))

    totalFramesReference = len(predictionImages)
    totalFramesUser = len(usrImages)
    usrImagesCopy = usrImages.copy()
    refImagesCopy = predictionImages.copy()
    matched = []

    for rImg in predictionImages:
        usrImages = usrImagesCopy.copy()

        for uImg in usrImages:

            if distance is not None:
                # Get the position of the reference frame.
                rFrameName = ntpath.basename(rImg)
                rFramePosition = re.findall(r'\d+', rFrameName)[0]

                # Get the position of the user frame.
                uFrameName = ntpath.basename(uImg)
                uFramePosition = re.findall(r'\d+', uFrameName)[0]

                if abs(int(rFramePosition) - int(uFramePosition)) > distance:
                    continue

            first = cv2.imread(rImg)
            second = cv2.imread(uImg)

            hsv_first = cv2.cvtColor(first, cv2.COLOR_BGR2HSV)
            hsv_second = cv2.cvtColor(second, cv2.COLOR_BGR2HSV)

            hist_first = cv2.calcHist([hsv_first], channels, None, histSize, ranges, accumulate=False)
            cv2.normalize(hist_first, hist_first, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

            hist_second = cv2.calcHist([hsv_second], channels, None, histSize, ranges, accumulate=False)
            cv2.normalize(hist_second, hist_second, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

            diff = cv2.compareHist(hist_first, hist_second, cv2.HISTCMP_CORREL)

            if abs(diff) > epsilon:
                matched.append(rImg)
                refImagesCopy.remove(rImg)
                usrImagesCopy.remove(uImg)
                break

    totalMatched = len(matched)
    precision = 1.0 if totalFramesReference == 0 else totalMatched / totalFramesReference
    recall = 1.0 if totalFramesUser == 0 else totalMatched / totalFramesUser
    f1 = 0 if precision == 0 and recall == 0 else (2 * precision * recall) / (precision + recall)

    # Kappa
    nYmYr = totalMatched
    nNmYr = totalFramesReference - totalMatched
    nYmNr = totalFramesReference - totalMatched
    nNmNr = videoFrames - nYmYr - nNmYr - nYmNr

    pO = (nYmYr + nNmNr) / videoFrames

    pEn = ((nNmNr + nNmYr) / videoFrames) * (nNmNr + nYmNr) / videoFrames
    pEy = ((nYmYr + nYmNr) / videoFrames) * (nYmYr + nNmYr) / videoFrames
    pE = pEn + pEy
    kappa = (pO - pE) / (1 - pE)

    print('Comparing with', userFolder)
    print('Frames matched: ', totalMatched)
    print('Non-matched reference: ', len(refImagesCopy))
    print('Non-matched user: ', len(usrImagesCopy))
    print('F1:', f1)
    print('Kappa:', kappa)
    print('--------------')

    return f1, kappa


def computeCUS(
        epsilon,
        videoFrames,
        refPath=USER_SUMMARIES_FRAMES_BASE_PATH,
        predictionPath=AUTOMATIC_SUMMARY_FRAMES_PATH):
    predictionImages = sorted(glob.glob(predictionPath + '/*.*'))

    userFolders = list(filter(lambda x: os.path.isdir(refPath+ '/' + x), os.listdir(refPath)))
    average_f1 = 0
    average_kappa = 0

    for userFolder in userFolders:
        f1, kappa = computeMetrics(userFolder, predictionImages, refPath, epsilon, videoFrames, None)
        average_f1 = average_f1 + f1
        average_kappa = average_kappa + kappa

    average_f1 = average_f1 / len(userFolders)
    average_kappa = average_kappa / len(userFolders)
    return average_f1, average_kappa


def computeBHI(
        epsilon,
        videoFrames,
        distance,
        refPath=USER_SUMMARIES_FRAMES_BASE_PATH,
        predictionPath=AUTOMATIC_SUMMARY_FRAMES_PATH):
    predictionImages = sorted(glob.glob(predictionPath + '/*.*'))

    userFolders = list(filter(lambda x: os.path.isdir(refPath+ '/' + x), os.listdir(refPath)))
    average_f1 = 0
    average_kappa = 0

    for userFolder in userFolders:
        f1, kappa = computeMetrics(userFolder, predictionImages, refPath, epsilon, videoFrames, distance)
        average_f1 = average_f1 + f1
        average_kappa = average_kappa + kappa

    average_f1 = average_f1 / len(userFolders)
    average_kappa = average_kappa / len(userFolders)
    return average_f1, average_kappa
