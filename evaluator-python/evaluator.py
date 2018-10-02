import argparse
import h5py
import numpy as np
import cv2
import os
import shutil
import glob

AUTOMATIC_SUMMARY_FRAMES_PATH   = 'data/data'
USER_SUMMARIES_FRAMES_BASE_PATH = 'data/reference'

parser = argparse.ArgumentParser("Evaluator for OST")
parser.add_argument('-a', '--automatic_summarization', type=str, required=True)
parser.add_argument('-u', '--users_summarization', type=str, required=True)
parser.add_argument('-v', '--original_video', type=str, required=True)
parser.add_argument('-e', '--epsilon', type=float, required=True)
parser.add_argument('--user_summary_path', type=str, required=True, help="User summary path in the h5 file (ex video_11/user_summary)")
parser.add_argument('--automatic_summary_path', type=str, required=True, help="Automatic summary path in the h5 file (ex video_11/machine_summary)")

args = parser.parse_args()


# """ Returns the number of frames matched between
# both summarization.
# """
# def calc_marches(aSummary, uSummary, window=0):
#     if window == 0:
#         overlap = np.sum(aSummary * uSummary)
#     else:
#         overlap = 0
#
#     return overlap


def prepare_folders(uSummary, aSummary, video):
    vidcap = cv2.VideoCapture(video)
    total_summ_frames = len(aSummary)
    total_video_frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)

    print('Total video frames', total_video_frames)
    print('Total summ frames', total_summ_frames)

    if total_video_frames != total_summ_frames:
        print("Frames don't match")

    if os.path.exists('data'):
        shutil.rmtree('data')

    os.makedirs(AUTOMATIC_SUMMARY_FRAMES_PATH)
    os.makedirs(USER_SUMMARIES_FRAMES_BASE_PATH)

    aSelectedFrames = np.where(aSummary == 1.0)
    print('Genereting frames from automatic summary')
    for frame_id in aSelectedFrames[0]:
        print('writing frame', frame_id)
        vidcap.set(1,frame_id);
        ret, frame = vidcap.read()
        frame_name = AUTOMATIC_SUMMARY_FRAMES_PATH + '/frame' + str(frame_id) + '.jpg'
        cv2.imwrite(frame_name, frame)

    print('Genereting frames from user summaries. Total number of users: ', len(uSummary))
    for index, user in enumerate(uSummary):
        print('User' + str(index+1) + '...')
        os.makedirs(USER_SUMMARIES_FRAMES_BASE_PATH + '/user' + str(index+1))
        userFrames = np.where(user == 1.0)

        for frame_id in userFrames[0]:
            print('writing frame', frame_id)
            vidcap.set(1, frame_id);
            ret, frame = vidcap.read()
            frame_name = USER_SUMMARIES_FRAMES_BASE_PATH + '/user' + str(index+1) + '/frame' + str(frame_id).zfill(4) + '.jpg'
            cv2.imwrite(frame_name, frame)


def computeF1(userFolder, refImages, refPath, epsilon):
    h_bins = 50
    s_bins = 60
    histSize = [h_bins, s_bins]
    h_ranges = [0, 180]
    s_ranges = [0, 256]
    ranges = h_ranges + s_ranges # concat lists
    channels = [0, 1]

    usrImages = sorted(glob.glob(refPath + '/' + userFolder + '/*.jpg'))

    totalFramesReference = len(refImages)
    totalFramesUser = len(usrImages)
    usrImagesCopy = usrImages.copy()
    refImagesCopy = refImages.copy()
    matched = []

    for rImg in refImages:
        usrImages = usrImagesCopy.copy()

        for uImg in usrImages:
            first = cv2.imread(rImg)
            second = cv2.imread(uImg)

            hsv_first = cv2.cvtColor(first, cv2.COLOR_BGR2HSV)
            hsv_second = cv2.cvtColor(second, cv2.COLOR_BGR2HSV)

            hist_first = cv2.calcHist([hsv_first], channels, None, histSize, ranges, accumulate=False)
            cv2.normalize(hist_first, hist_first, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

            hist_second = cv2.calcHist([hsv_second], channels, None, histSize, ranges, accumulate=False)
            cv2.normalize(hist_second, hist_second, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

            diff = cv2.compareHist(hist_first, hist_second, cv2.HISTCMP_CORREL)

            if diff > epsilon:
                matched.append(rImg)
                refImagesCopy.remove(rImg)
                usrImagesCopy.remove(uImg)
                break

    totalMatched = len(matched)
    precision = totalMatched / totalFramesReference
    recall = totalMatched / totalFramesUser
    f1 = (2 * precision * recall) / (precision + recall)

    print('Comparing with', userFolder)
    print('Frames matched: ', totalMatched)
    print('Non-matched reference: ', len(refImagesCopy))
    print('Non-matched user: ', len(usrImagesCopy))
    print('F1:', f1)
    print('--------------')

    return f1


def computeCUS(refPath, predictionPath, epsilon):

    refImages = sorted(glob.glob(predictionPath + '/*.jpg'))

    userFolders = list(filter(lambda x: os.path.isdir(refPath+ '/' + x), os.listdir(refPath)))
    average_f1 = 0

    for userFolder in userFolders:
        average_f1 = average_f1 + computeF1(userFolder, refImages, refPath, epsilon)

    average_f1 = average_f1 / len(userFolders)
    print('Average F1:', round(average_f1, 2))


if __name__ == '__main__':
    uFile = h5py.File(args.users_summarization, 'r')
    aFile = h5py.File(args.automatic_summarization, 'r')

    # Access user summaries table in H5
    user_summaries = uFile
    for tableName in args.user_summary_path.split('/'):
        user_summaries = user_summaries[tableName]

    # Access automatic summaries table in H5
    automatic_summary = aFile
    for tableName in args.automatic_summary_path.split('/'):
        automatic_summary = automatic_summary[tableName]

    prepare_folders(user_summaries, automatic_summary, args.original_video)

    computeCUS(
        USER_SUMMARIES_FRAMES_BASE_PATH,
        AUTOMATIC_SUMMARY_FRAMES_PATH,
        args.epsilon
    )
