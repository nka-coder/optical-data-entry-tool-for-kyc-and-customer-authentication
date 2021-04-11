from fastapi import FastAPI, File, Form, UploadFile
import shutil
import time
from id_reader_utilities import unit_extraction, count_inaccuracy
from id_reader_utilities import filter_mrz, mrz_improver, check_mrz_all_info, parse_mrz
from create_dataset import api_video_to_image
import os
from os import listdir

# Defining the format of an MRZ
MRZ_FORMAT = {
  "mrz_type": "TD3",
  "type": "P",
  "country": "D",
  "number": "CO1XOOT47",
  "check_number": "8",
  "date_of_birth": "640812",
  "check_date_of_birth": "5",
  "expiration_date": "270228",
  "check_expiration_date": "3",
  "nationality": "D",
  "sex": "F",
  "names": "ERIKA",
  "surname": "MUSTERMANN"
}

app = FastAPI()

@app.get('/')
async def index():
    return {'key':'value'}


@app.post('/idreader')
async def id_reader(file: UploadFile = File(...) ):
    """
    This function extract identity information from a video of an identity document containing an MRZ.

    Input parameters:
    - file: video of an identity document containing an MRZ

    Return:
    - mrz: dictionary containing identity information extracted from the input video
    - message: the status of execution the function (Success or Failed)
    """
    print('received')
    sample_size = 5
    checked_digits_mrz = {}

    # Generate dataset of images from the input video
    message = 'Failed'
    images_folder = 'Temp/'+file.filename.replace('.mp4','').replace('.MOV','')
    new_video = str(time.time())+file.filename

    with open(new_video, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    message = api_video_to_image('', new_video, images_folder)

    # Extract identity information from the generated images
    filename_list = listdir(images_folder)
    mrz_list = []
    counter = 0
    for image in filename_list:       
        try:
            mrz_data = unit_extraction(images_folder,image, MRZ_FORMAT)
            if counter < sample_size :
                mrz_list.append(mrz_data)
                counter +=1
            else:
                mrz_list.append(mrz_data)
                improved_mrz = mrz_improver(mrz_list, MRZ_FORMAT)
                improved_parsed_mrz = parse_mrz(improved_mrz, MRZ_FORMAT)
                counter = 0
                if check_mrz_all_info(improved_parsed_mrz) :
                    checked_digits_mrz = improved_parsed_mrz
                    message = 'Success'
                    break
                else:
                    checked_digits_mrz = {}
        except:
            pass
    
    # Delete images and folder generated earlier to extract identity information
    for image in filename_list: 
        os.remove(images_folder+'/'+image)

    os.remove(new_video)
    os.rmdir(images_folder)

    return {'mrz':checked_digits_mrz, 'message': message}

