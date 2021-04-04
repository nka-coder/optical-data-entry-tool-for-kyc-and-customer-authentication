# Importing all necessary libraries
import os
from os import listdir
import cv2


def video_to_image(video_folder,category):

    filename_list = listdir(video_folder)
    for filename in filename_list:

        # Read the video from specified path
        cap = cv2.VideoCapture(video_folder+filename)

        try:

            # creating a folder named data
            if not os.path.exists('data/train/'+category):
                os.makedirs('data/train/'+category)
                
            if not os.path.exists('data/test/'+category):
                os.makedirs('data/test/'+category)

            if not os.path.exists('data/valid/'+category):
                os.makedirs('data/valid/'+category)

            # if not created then raise error
        except OSError:
            print ('Error: Creating directory of data')

        # frame
        currentframe = 0
        splitter =0
        spacing = 0
        while(True):
            # reading from frame
            ret,frame = cap.read()
            spacing +=1
            if spacing ==9:
                if ret :
                    print('Reached here3')
                    # if video is still left continue creating imagesl
                    if splitter < 7:
                        name = './data/train/'+category+'/'+ filename.replace('.mp4','').replace('.MOV','')+'_'+str(currentframe) + '.jpg'
                        print ('Creating...' + name)
                        # writing the extracted images
                        cv2.imwrite(name, frame)
                    if splitter > 6 and splitter < 9:
                        name = './data/valid/'+category+'/' + filename.replace('.mp4','').replace('.MOV','')+'_'+str(currentframe) + '.jpg'
                        print ('Creating...' + name)
                        # writing the extracted images
                        cv2.imwrite(name, frame)

                    if splitter > 8:
                        name = './data/test/'+category+'/' + filename.replace('.mp4','').replace('.MOV','')+'_'+str(currentframe) + '.jpg'
                        print ('Creating...' + name)
                        # writing the extracted images
                        cv2.imwrite(name, frame)
                        splitter = 0
                    if splitter >9:
                        splitter=-1

                    splitter +=1
                    # increasing counter so that it will
                    # show how many frames are created
                    currentframe += 1
                    spacing = 0
                else:
                    break

            # Release all space and windows once done
        cap.release()
        cv2.destroyAllWindows()

video_to_image('video/albania_identity_card/videos/','1')
video_to_image('video/usa_passport_card/videos/','2')
video_to_image('video/brazil_passport_card/videos/','3')