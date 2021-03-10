import zipfile
import os

folder = "video/albania_identity_card"
if not os.path.exists(folder):
       os.makedirs(folder)

with zipfile.ZipFile("albania_identity_card.zip","r") as zip_ref:
    zip_ref.extractall(folder)