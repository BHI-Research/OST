from __future__ import print_function
import argparse
import h5py
import cv2

from metrics import prepare_folders, computeCUS, computeBHI

parser = argparse.ArgumentParser("Evaluator for OST")
parser.add_argument('-a', '--automatic_summarization', type=str, required=True)
parser.add_argument('-u', '--users_summarization', type=str, required=True)
parser.add_argument('-v', '--original_video', type=str, required=True)
parser.add_argument('-e', '--epsilon', default=0.4, type=float)
parser.add_argument('-d', '--distance', default=120, type=int)
parser.add_argument('-m', '--method', type=str, required=True, default='bhi', choices=['cus', 'bhi'])
parser.add_argument('--user_summary_path', type=str, required=True, help="User summary path in the h5 file (ex video_11/user_summary)")
parser.add_argument('--automatic_summary_path', type=str, required=True, help="Automatic summary path in the h5 file (ex video_11/machine_summary)")

args = parser.parse_args()


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
    automatic_summary = automatic_summary[:]

    prepare_folders(user_summaries, automatic_summary, args.original_video)

    cap = cv2.VideoCapture(args.original_video)
    videoLength = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if args.method == 'cus':
        f1, kappa = computeCUS(
            args.epsilon,
            videoLength
        )
    else:
        f1, kappa = computeBHI(
            args.epsilon,
            videoLength,
            args.distance
        )

    print('Average F1:', round(f1, 2))
    print('Average Kappa:', round(kappa, 2))
