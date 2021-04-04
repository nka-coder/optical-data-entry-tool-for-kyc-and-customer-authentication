import zipfile
import os
"""
This program helps to unzip zipped a folder
"""
# Set destination folder
folder = "video/brazil_paasport_card"
if not os.path.exists(folder):
       os.makedirs(folder)

# perform unzip task
with zipfile.ZipFile("video/brazil_passport_card/braszil_passport_card.zip","r") as zip_ref:
    zip_ref.extractall(folder)