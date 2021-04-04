# Importing all necessary libraries
import os
from os import listdir
import cv2


def experiment_video_to_image(video_folder, dest):
    """
    This function create a dataset of images from a video.
    
    Input parameters:
    - video_folder: path to the folder containing videos of the passport that need identity
                    information extraction.
    - dest: path to the folder in which images generated from the video are stored.

    Return: None
    """

    filename_list = listdir(video_folder)
    for filename in filename_list:

        # Read the video from specified path
        cap = cv2.VideoCapture(video_folder+filename)

        try:
            # creating the folder in wich the images will be stored
            if not os.path.exists('data/'+dest):
                os.makedirs('data/'+dest)

        except OSError:
            print ('Error: Creating directory of data')

        currentframe = 0
        spacing = 0
        while(True):
            # reading from frame
            ret,frame = cap.read()
            spacing +=1
            if spacing ==4:
                if ret :
                    name = './data/'+dest+'/'+ filename.replace('.mp4','').replace('.MOV','')+'_'+str(currentframe) + '.jpg'
                    print ('Creating...' + name)
                    # writing the extracted images
                    cv2.imwrite(name, frame)
                    currentframe +=1
                    spacing = 0
                else:
                    break

        cap.release()
        cv2.destroyAllWindows()




def api_video_to_image(video_folder, filename, dest):
    """
    This function create a dataset of images from a video. Then
    
    Input parameters:
    - video_folder: path to the folder containing videos of the passport that need identity
                    information extraction.
    - filename: name of the video from which the images are generated.
    - dest: path to the folder in which images generated from the video are stored.

    Return: 
    - message: the status of execution the function (Success or Error)
    """

    # Read the video from specified path
    cap = cv2.VideoCapture(video_folder+filename)
    message = 'Failed: Cannot generate images from the video'
    
    try:
        # creating the folder in wich the images will be stored
        if not os.path.exists(dest):
            os.makedirs(dest)
        
    except OSError:
        message = 'Error: Creating directory of data'

    currentframe = 0
    spacing = 0
    while(True):
        # reading from frame
        ret,frame = cap.read()
        spacing +=1
        if spacing ==4:
            if ret :
                name = './'+dest+'/'+ filename.replace('.mp4','').replace('.MOV','')+'_'+str(currentframe) + '.jpg'
                # writing the extracted images
                cv2.imwrite(name, frame)
                currentframe +=1
                spacing = 0
            else:
                message = 'Success'
                break

    cap.release()
    cv2.destroyAllWindows()
    return message