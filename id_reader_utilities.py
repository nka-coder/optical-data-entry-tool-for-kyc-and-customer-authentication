# Import PassportEye
from passporteye import read_mrz
import pytesseract
from PIL import Image, ImageEnhance
import os
from os import listdir
import cv2
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def unit_extraction(image_folder,image_sample, mrz_format):
    """
    This function implements Passporteye read_mrz() function to extract identity information
    from the MRZ of an identity document.

    Input parameters:
    - image_folder: path to the folder containing the image of the identity document 
    - image_sample: name of the image of the identity document containing information to extract
    - mrz_format: format of an MRZ
    Example:
    valid_mrz  = {
                    "mrz_type": "TD3",
                    "type": "P",
                    "country": "CMR",
                    "number": "01312168",
                    "check_number": "4",
                    "date_of_birth": "830408",
                    "check_date_of_birth": "1",
                    "expiration_date": "140611",
                    "check_expiration_date": "5",
                    "nationality": "CMR",
                    "sex": "M",
                    "names": "ADAMOU",
                    "surname": "NCHANGE KOUOTOU"
                }

    Return:
    - mrz_data: dictionary containing identity information extacted
    """
    
    # Process image
    mrz = read_mrz(image_folder + '/' + image_sample)
    mrz_data = filter_mrz(mrz.to_dict(), mrz_format)

    return mrz_data

def mrz_improver(mrz_list, mrz_format):
    """
    This function implements the Maximum likelihod of character algorithm to extract identity information
    from the MRZ of an identity document.

    Input parameters:
    - mrz_list: list containing a set of MRZ dictionary. 
    - mrz_format: format of an MRZ

    Return:
    - mrz: improved extraction of identity information according to Maximum likelihood of characters 
            algorithm
    """
    mrz = {}
    for key in mrz_format.keys():
        info_sample_len = []
        info_sample = []
        for i in range(len(mrz_list)):
            info_sample_len.append(len(mrz_list[i][key]))
            info_sample.append(mrz_list[i][key])
        
        while('' in info_sample):
            info_sample.remove('')

        #if key == 'surname':
            #print(info_sample)

        info_maximized = ""
        text_lenght = max(info_sample_len)
        
        for i in range(text_lenght):
            character_list = []
            for j in range(len(info_sample)):
                try:
                    character_list.append(info_sample[j][i])
                except:
                    character_list.append('<')

            max_occ = max(character_list, key = character_list.count)
            info_maximized = info_maximized + max_occ
        mrz[key] = info_maximized
    
    return mrz

def parse_mrz(mrz, mrz_format):
    """
    This function parse each field of an MRZ dictionary to improve the quality of identity
    information stored in it. 

    Input parameters:
    - mrz: MRZ dictionary. 
    - mrz_format: format of an MRZ

    Return:
    - mrz: improved MRZ dictionary
    """
    mrz_parsed = {}
    for key in mrz_format.keys():
        if key == 'surname' or key == 'name':
            mrz_parsed[key] = mrz[key].split(' K ')[0]
        else:
            mrz_parsed[key] = mrz[key]

        mrz_parsed[key] = mrz_parsed[key].split('  ')[0]
        mrz_parsed[key] = mrz_parsed[key].replace('<','')

    return mrz_parsed

def check_mrz_info(mrz_value, mrz_check_value):
    """
    This function implement the verification rule for check-digits of a MRZ

    Input parameters:
    mrz_value: information to check
    mrz_check_value: value of the check-digit to obtain after computation of the rule on 'mrz_value'

    Return: True or False
    """
    info = str(mrz_value)
    checker = 0
    alpha_to_num = {c: 10 +i for i, c in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}
    for i, c in enumerate(info):
        if i % 3 == 0:
            weight = 7
        elif i % 3 == 1:
            weight = 3
        else:
            weight = 1

        if c == '<':
            val = 0
        elif c.isalpha():
            val = alpha_to_num[c]
        else:
            val = int(c)

        checker += val*weight

    return str(checker % 10) == str(mrz_check_value)

def check_mrz_all_info(mrz):
    """
    This function implement check-digit verification for date_of_birth, expiration_date,
    sex, name and surname of an MRZ dictionary.

    Input parameter: MRZ dictionary

    Return: True or False
    """
    result = True
    #if not check_mrz_info(mrz["number"], mrz["check_number"]):
        #result = False

    if not check_mrz_info(mrz["date_of_birth"], mrz["check_date_of_birth"]):
        result = False

    if not check_mrz_info(mrz["expiration_date"], mrz["check_expiration_date"]):
        result = False

    if mrz["sex"] != 'M' and  mrz["sex"] != 'F':
        result = False

    if 'KKK' in mrz["names"]  or 'KKK' in mrz["surname"]:
        result = False
  
    return result 


def dataset_size(mrz, actual_mrz):
    """
    This function determines the adjusted dataset size

    Input parameters:
    - MRZ dictionary
    - mrz_format: Actual identity information information into the identity document. Its format is
                described below
    Example:
    valid_mrz  = {
                    "mrz_type": "TD3",
                    "type": "P",
                    "country": "CMR",
                    "number": "01312168",
                    "check_number": "4",
                    "date_of_birth": "830408",
                    "check_date_of_birth": "1",
                    "expiration_date": "140611",
                    "check_expiration_date": "5",
                    "nationality": "CMR",
                    "sex": "M",
                    "names": "ADAMOU",
                    "surname": "NCHANGE KOUOTOU"
                }

    Return: 
    - count: adjusted dataset size
    """
    count1 = 0
    for key in mrz.keys():
        count1 += len(mrz[key])

    count2 = 0
    for key in mrz.keys():
        count2 += len(actual_mrz[key])

    count = max(count1, count2)
    return count

def count_inaccuracy(extracted_mrz, actual_mrz):
    """
    This count the number of discrepency of characters between two MRZ dictionaries
    Return: 
    - true_negative: number of discrepency of characters
    """
    true_negative = 0
    for key in actual_mrz.keys():
        if extracted_mrz[key] == actual_mrz[key]:
            true_negative += 0
        else:
            size = max([len(extracted_mrz[key]),len(actual_mrz[key])])
            for i in range(size):
                try:
                    if extracted_mrz[key][i] != actual_mrz[key][i]:
                        true_negative +=1
                except:
                    true_negative +=1

    return true_negative

def filter_mrz(extracted_mrz, actual_mrz):
    """
    This function remove unused field from a MRZ dictionary.

    Input parameters:
    - extracted_mrz : MRZ dictionary that contain unused field
    - actual_mrz : MRZ dictionary format that serve as benchmark for unused field removal

    Return:
    - mrz: extracted_mrz with unused field removed.
    """
    mrz = {}
    for key in actual_mrz.keys():
        mrz[key] = extracted_mrz[key]
    return mrz

