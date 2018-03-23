#!/usr/bin/env python
import h5py
import pandas as panda
import tables
import ntpath
import cv2
import os
import csv
import numpy as np
import argparse
from datetime import datetime
import argparse
from os import walk
from sys import exit
import os.path as path

from utils import print_object_in_file
# from utils import output_label

class get_parameters(object):
	pass

"""
Parameters:
	
	parameters.video
	parameters.users_csv
	parameters.vsum_csv
	parameters.method
	parameters.format
	parameters.quality
	parameters.offset
	parameters.epsilon
	parameters.distance
	parameters.users
	parameters.video_length
	parameters.output_path

"""


#/*********************************************************************************************    
def get_args():
    parser = argparse.ArgumentParser(description='OSM UTN FRBB')

    parser.add_argument(
        'video',
        type = str,
        help = 'Video name, including file extension'
    )
    parser.add_argument(
        'users_csv',
        type = str,
        help = 'CSV with users sumarization'
    )
    parser.add_argument(
        'vsum_csv',
        type = str,
        help = 'CSV with video sumarization we want to evaluate'
    )
    parser.add_argument(
        '-cus', '--cus',
        action = 'store_true',
        help = 'Run CUS metric'
    )
    parser.add_argument(
        '-bhi', '--bhi',
        action = 'store_true',
        help = 'Run BHI metric'
    )
    parser.add_argument(
        '-e', nargs = '?',
        type = float,
        help = 'Epsilon'
    )
    parser.add_argument(
        '-d', nargs = '?',
        type = int,
        help = 'Distance parameter for bhi method'
    )
    parser.add_argument(
        '-u', nargs = '?',
        type = int,
        help = 'Number of users'
    )


    parser.add_argument('-f', '--format', nargs='?',   help='File format of the output frames')
    parser.add_argument('-q', nargs='?',  choices=range(0, 100), type=int, help='The JPG quality rate')
    parser.add_argument('-offset', nargs='?',  type=int, help='The frame selection offset ')

    parser.add_argument('-ush', '--updatesh', action='store_true', help='No make a new sh, only update')


    return vars(parser.parse_args())
    



#/*********************************************************************************************    

def process_args():

	args = get_args()

	"""
	print args['bhi']
	print args['cus']
	print args['u']
	print args['users_csv']
	print args['d']
	print args['format']
	print args['vsum_csv']
	print args['q']
	print args['video']
	print args['offset']
	print args['e']
	"""



	parameters = get_parameters()



	setattr(parameters, 'video', args['video'])		
	setattr(parameters, 'users_csv', args['users_csv'])		
	setattr(parameters, 'vsum_csv', args['vsum_csv'])		



	if(args['bhi'] and args['cus']):
		print "DUAL EVALUATION INPUT"


	if(args['cus']):
		setattr(parameters, 'method', 1)	
	if(args['bhi']):
		setattr(parameters, 'method', 0)	

	if(args['format']):
		setattr(parameters, 'format', args['format'])
	else:
		setattr(parameters, 'format', "jpg")

	if(args['q']):
		setattr(parameters, 'quality', args['q'])
	else:
		setattr(parameters, 'quality', 0)

	if(args['offset']):
		setattr(parameters, 'offset', args['offset'])
	else:
		setattr(parameters, 'offset', 0)

	if(args['e']):
		setattr(parameters, 'epsilon', args['e'])
	else:
		setattr(parameters, 'epsilon', 0.5)

	if(args['d']):
		setattr(parameters, 'distance', args['d'])
	else:
		setattr(parameters, 'distance', 120)

	if(args['u']):
		setattr(parameters, 'users', args['u'])
	else:
		setattr(parameters, 'users', 5)

	if(args['updatesh']):
		setattr(parameters, 'updatesh', 1)
	else:
		setattr(parameters, 'updatesh', 0)





	return parameters



#/*********************************************************************************************    


"""Open a CSV file and returns a matrix."""
def csv_to_matrix(file):
    csv_file = open(file + '.csv', "rb")
    output = np.array(list(
        csv.reader(csv_file, delimiter=",")
    ))

    return output


#/*********************************************************************************************    



"""Returns 1 if csv is binary. Otherwise, returns 0"""
def count_zeros(file_csv):
    frames = csv_to_matrix(file_csv)
    zeros = 0
    binary_flag = 0

    for i in frames[0]:
        if i == '0':
            zeros += 1
        if zeros > 2:
            binary_flag = 1
            break

    return binary_flag


"""Determines the format of the CSVs.
If 0, files contain keyframes.
If 1, files are binaries (1s & 0s)
Otherwise, returns 2 (file not supported).
"""
def is_binary_selection(users_csv, vsum_csv):
    files_binary = 0
    file_binary_user = 0
    file_binary_vsum = 0

    file_binary_user = count_zeros(users_csv)
    file_binary_vsum = count_zeros(vsum_csv)

    print file_binary_user
    print file_binary_vsum

    if file_binary_user and file_binary_vsum:
        files_binary = 1
    elif file_binary_user == file_binary_vsum:
        files_binary = 0
    else:
        files_binary = 2
        print "Conflict with CSV files format"

    return files_binary


#/*********************************************************************************************    

#Array to Frame without  Frame ID
def get_frame_without_ID(parameters):

    VIDEO_PATH      = parameters.video
    USERS_CSV       = parameters.users_csv
    VSUM_CSV        = parameters.vsum_csv
    FORMAT          = parameters.format
    FRAME_ID_OFFSET = parameters.offset
    JPEG_QUALITY    = parameters.quality

    cap = cv2.VideoCapture(VIDEO_PATH)

    if cap:
        print "VIDEO OPENED"
    else:
        print "VIDEO NOT FOUND"

    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) #Video Lenght
    fps =  int(cap.get(cv2.CAP_PROP_FPS)) #Videl Lenght
    time_length = float(length/fps)

    print "lenght" , length
    print "fps" , fps
    print "time_lenght" , time_length

    frames = np.array(csv_to_matrix(USERS_CSV))

    # Get the video name from path.
    video_name = os.path.basename(VIDEO_PATH)

    # Remove the file extension.
    video_name = video_name.split('.')[0]

    OUTPUT_FOLDER_NAME = 'output'

    if not os.path.exists(OUTPUT_FOLDER_NAME):
        os.makedirs(OUTPUT_FOLDER_NAME)

    main_folder_output = os.path.join(OUTPUT_FOLDER_NAME, video_name)


    setattr(param, 'output_path', main_folder_output)

    reference_exist = 0

    if os.path.exists(main_folder_output) == 0:     
            os.mkdir(main_folder_output)
    else:
            print 'DIRECTORY', main_folder_output , 'EXISTS'

    references_folder = main_folder_output + '/' + 'reference'
    if os.path.exists(references_folder) == 0:      
            os.mkdir(references_folder)
    else:
            print 'DIRECTORY', references_folder , 'EXISTS'
            reference_exist=1

    data_folder = main_folder_output + '/' + 'data'
    if os.path.exists(data_folder) == 0:        
            os.mkdir(data_folder)
    else:
            print 'DIRECTORY', data_folder , 'EXISTS'
            
    n_users = frames.shape[0]


    if reference_exist:

            return length

    
    for user in range(0,n_users):

            frame_detection=0
            frame_id=0
            length_array=len(frames[user])	

            folder_output=references_folder +'/' + "user" + "%d" % (user+1 )

            if os.path.exists(folder_output) == 0:          
                    os.mkdir(folder_output)
            else:
                    print 'DIRECTORY', folder_output , 'EXISTS'


            while (cap.isOpened()):
                    
                    ret, frame = cap.read()		

                    if int(frames[user][frame_id])==1:
    
                            #The first argument of cap.set(), number 2 defines that parameter for setting the frame selection.
                            #Number 2 defines flag CV_CAP_PROP_POS_FRAMES which is a 0-based index of the frame to be decoded/captured next.
                            #The second argument defines the frame number in range 0.0-1.0
                            cap.set(1,frame_id+FRAME_ID_OFFSET);

                            #Read the next frame from the video. If you set frame 749 above then the code will return the last frame.
                            ret, frame = cap.read()
                    
                            frame_name = folder_output + '/' + 'Frame%d' % (frame_id)	  + '.' + FORMAT 

                            if(JPEG_QUALITY!=0)	:
                                    cv2.imwrite(frame_name, frame, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])		
                            else:
                                    cv2.imwrite(frame_name, frame)
                            frame_detection+=1		

                    frame_id+=1

                    if frame_id>len(frames[user])-1:
                            break;
                    if frame_id==length:   
                                    #print 'END OF VECTOR'      
                                    break
            
            print 'USER',user+1 ,'FRAMES DETECTED:',frame_detection

    #***************************************************************
    #***************************************************************

    # if not parameters.lfovs:
            
    frame_id=0

    folder_output=data_folder
    frames_VSUM=np.array(csv_to_matrix(VSUM_CSV)) 

    length_array=len(frames_VSUM[0])

            
    if os.path.exists(folder_output) == 0:
            os.mkdir(folder_output)
    else:
            print 'DIRECTORY', folder_output, 'EXISTS'
    
    frame_detection	=0

    while (cap.isOpened()):	
    
            if int(frames_VSUM[0][frame_id])==1:
                    
                    
                    #The first argument of cap.set(), number 2 defines that parameter for setting the frame selection.
                    #Number 2 defines flag CV_CAP_PROP_POS_FRAMES which is a 0-based index of the frame to be decoded/captured next.
                    #The second argument defines the frame number in range 0.0-1.0
                    cap.set(1,frame_id+FRAME_ID_OFFSET);
                    #Read the next frame from the video. If you set frame 749 above then the code will return the last frame.
                    ret, frame = cap.read()
                    
                    frame_name = folder_output + '/' + 'Frame%d' % (frame_id)	  + '.' + FORMAT      
                    if(JPEG_QUALITY!=0)	:
                                    cv2.imwrite(frame_name, frame, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])		
                    else:
                                    cv2.imwrite(frame_name, frame)
                    frame_detection+=1
                    
            
            frame_id+=1
            if frame_id>len(frames_VSUM[0])-1:
                            break;
            if frame_id==length:   
                    #print 'END OF VECTOR'      
                    break
    
    print 'FRAMES DETECTED:',frame_detection

    cap.release()
    return length



#Array to Frame with Frame ID
#Arreglos de numeros de ID de keyframes
def get_frame_with_ID(parameters):

	VIDEO_PATH=	parameters.video
	USERS_CSV=	parameters.users_csv
	VSUM_CSV=	parameters.vsum_csv
	FORMAT =  	parameters.format
	FRAME_ID_OFFSET =  	parameters.offset
	JPEG_QUALITY = parameters.quality
	"""
	parameters.video
	parameters.users_csv
	parameters.vsum_csv
	parameters.method
	parameters.format
	parameters.quality
	parameters.offset
	parameters.epsilon
	parameters.distance
	parameters.users
	parameters.video_length
	parameters.output_path
	"""

	cap = cv2.VideoCapture(VIDEO_PATH)

	if cap:
		print "VIDEO OPENED"
	else:
		print "VIDEO NOT FOUND"

	length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) #Videl Lenght
	fps =  int(cap.get(cv2.CAP_PROP_FPS)) #Videl Lenght
	time_length = float(length/fps)

	print "lenght" , length
	print "fps" , fps
	print "time_lenght" , time_length



	frames=np.array(csv_to_matrix(USERS_CSV)) 


        # Get the video name from path.
        video_name = os.path.basename(VIDEO_PATH)

        # Remove the file extension.
        video_name = video_name.split('.')[0]

        OUTPUT_FOLDER_NAME = 'output'

        if not os.path.exists(OUTPUT_FOLDER_NAME):
            os.makedirs(OUTPUT_FOLDER_NAME)

        main_folder_output = os.path.join(OUTPUT_FOLDER_NAME, video_name)

	# main_folder_output=VIDEO_PATH
        #
	# main_folder_output = main_folder_output.split('/')[3] #Elminate the ../../ +
        #
	# main_folder_output = main_folder_output.split('.')[0] #Elminate the file extension
        #
	# #main_folder_output = "../../output/" + main_folder_output #Run from osm_utility folder
        #
	# main_folder_output = "../output/" + main_folder_output


	setattr(param, 'output_path', main_folder_output)

	print main_folder_output

	reference_exist=0

	if os.path.exists(main_folder_output) == 0:		
		os.mkdir(main_folder_output)
	else:
		print 'DIRECTORY', main_folder_output , 'EXISTS'

	references_folder = main_folder_output + '/' + 'reference'
	if os.path.exists(references_folder) == 0:		
		os.mkdir(references_folder)
	else:
		print 'DIRECTORY', references_folder , 'EXISTS'
		reference_exist=1

	data_folder = main_folder_output + '/' + 'data'
	if os.path.exists(data_folder) == 0:		
		os.mkdir(data_folder)
	else:
		print 'DIRECTORY', data_folder , 'EXISTS'

	
	
	n_users = frames.shape[0]
	
	
	if reference_exist:

		return length


	for user in range(0,n_users):

		frame_id=0
		length_array=len(frames[user])
		frame_detection=0;

		folder_output=references_folder +'/' + "user" + "%d" % (user+1 )

		if os.path.exists(folder_output) == 0:			
			os.mkdir(folder_output)
		else:
			print 'DIRECTORY', folder_output , 'EXISTS'

		while (cap.isOpened()):
			
			ret, frame = cap.read()
			#print 'id',frame_id,'  detect',frame_detection 
			if frame_detection==length_array:
				break

			if int(frames[user][frame_detection])==frame_id:
				#print 'frame detected' , frame_id

				#frame_no = float(length-1) /(time_length*fps)
				print frame_id
				#The first argument of cap.set(), number 2 defines that parameter for setting the frame selection.
				#Number 2 defines flag CV_CAP_PROP_POS_FRAMES which is a 0-based index of the frame to be decoded/captured next.
				#The second argument defines the frame number in range 0.0-1.0
				cap.set(1,frame_id+FRAME_ID_OFFSET);

				#Read the next frame from the video. If you set frame 749 above then the code will return the last frame.
				ret, frame = cap.read()
				
				frame_name = folder_output + '/' + 'Frame%d' % (frame_id)	 + '.' + FORMAT
				if(JPEG_QUALITY!=0)	:
					cv2.imwrite(frame_name, frame, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])		
				else:
					cv2.imwrite(frame_name, frame)
				#cv2.imwrite(frame_name, frame)
				frame_detection+=1

			frame_id+=1

			if frame_id==length:   
					#print 'END OF VECTOR'      
					break
		
		print 'USER',user+1 ,'FRAMES DETECTED:',frame_detection

	#vsum


	# if not parameters.lfovs:

        frame_id=0

        frame_detection=0;

        folder_output=data_folder
        frames_VSUM=np.array(csv_to_matrix(VSUM_CSV)) 

        length_array=len(frames_VSUM[0])

                
        if os.path.exists(folder_output) == 0:
                os.mkdir(folder_output)
        else:
                print 'DIRECTORY', folder_output, 'EXISTS'

                
        while (cap.isOpened()):
                        

                #print 'id',frame_id,'  detect',frame_detection 
                if frame_detection==length_array:
                        break
                if int(frames_VSUM[0][frame_detection])==frame_id:
                        #print 'frame detected' , frame_id
                        
                        #The first argument of cap.set(), number 2 defines that parameter for setting the frame selection.
                        #Number 2 defines flag CV_CAP_PROP_POS_FRAMES which is a 0-based index of the frame to be decoded/captured next.
                        #The second argument defines the frame number in range 0.0-1.0
                        cap.set(1,frame_id+FRAME_ID_OFFSET);
                        #Read the next frame from the video. If you set frame 749 above then the code will return the last frame.
                        ret, frame = cap.read()
                        
                        frame_name = folder_output + '/' + 'Frame%d' % (frame_id)	  + '.' + FORMAT
                        if(frame_id<length):
                                if(JPEG_QUALITY!=0)	:
                                        cv2.imwrite(frame_name, frame, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])	
                                else:
                                        cv2.imwrite(frame_name, frame)	
                        #cv2.imwrite(frame_name, frame)
                        frame_detection+=1
                
                frame_id+=1

                if frame_id==length:   
                        #print 'END OF VECTOR'      
                        break
		

	cap.release()
	return length


#************************************************************************************************************

def create_sh(parameters, path):
    epsilon = parameters.epsilon
    distance = parameters.distance
    users = parameters.users
    length = parameters.video_length

    video_name = parameters.video

    method = parameters.method

    file = open('run.sh','w')

    if method == False:
        print "Generating RUN.SH for BHI"
        file.write('echo "Evaluating the video: ' +video_name+ ' with BHI"\n')
        file.write('echo "Distance: ' + str(distance) + '"\n')
    else:
        print "Generating RUN.SH for CUS"
        file.write('echo "Evaluating the video: ' +video_name+ ' with CUS"\n')

    file.write('echo "Epsilon: ' + str(epsilon) + '"\n')
    file.write('echo "Users: ' + str(users) + '"\n')
    file.write('echo "Simple zone"\n')

    if method == False:
        command_2 ='../build/osm --method bhi -e {0} -d {1} -n {2} -f {3} -r "{4}/reference" -i "{4}/data/"\n'
        file.write(
            command_2.format(epsilon, distance, users, length, parameters.output_path)
        )
    else:
        command_2 = '../build/osm --method cus -e {0} -n {1} -f {2} -r "{3}/reference" -i "{3}/data/"\n'
        file.write(
            command_2.format(epsilon, users, length, parameters.output_path)
        )

    file.close()


#************************************************************************************************************

def multiple_metric(parameters):

    vsumm_files=0
    video_files=0
    users_files=0
    for (path, ficheros, archivos) in walk(parameters.video):
        video_files=len(archivos)
    for (path, ficheros, archivos) in walk(parameters.users_csv):
        users_files =len(archivos)
    for (path, ficheros, archivos) in walk(parameters.vsum_csv):
        vsumm_files=len(archivos)

    if video_files != users_files or users_files != vsumm_files:
        print "PROBLEM WITH FILES"
        print "vsumm_files = ",vsumm_files
        print "users_files = ",users_files
        print "video_files = ",video_files

    video_names=[]

    for (path, ficheros, archivos) in walk(parameters.video):
        for i in range (0,len(archivos)):
            if len(archivos[i])>1:			
                video_names.append(archivos[i])
                #eval_files2.append(archivos[i].split('.')[0])

    return video_names


if __name__ == '__main__':

    param = process_args()

    binary_flag = is_binary_selection(param.users_csv, param.vsum_csv)

    if binary_flag == 1: #File with 0s & 1s
        video_length = get_frame_without_ID(param)
    elif binary_flag == 0: #File with frame numbers
        video_length = get_frame_with_ID(param)
    else:
        print "PROBLEM WITH CSV INPUT FORMAT"
        exit()

    setattr(param, 'video_length', video_length)

    # @TODO: Decide whether this is relevant or not. (output.txt)
    # output_label(param)

    # @TODO: Decide whether it's useful to update the sh file.
    # if param.updatesh:
    #     if path.exists('run.sh'):
    #         addline_sh(param)
    #     else:
    #         create_sh(param, 0)
    # else:
    create_sh(param, 0)

    print "FINISHED"
