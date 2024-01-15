"""
If you want to move many files between directory you can run this python script.
"""

import os
import shutil
import pandas as pd

mass_csv_path = r'd:\ML_Final_Project\ml\ML_Team28\datasets\table\clean_metadata_fixed.csv'
preprocess_file_source = r'D:\ML_Final_Project\ml\ML_Team28\datasets\image\clean_preprocess_png'
train_file_destination = r'd:\ML_Final_Project\yolo_code\yolov7\datasets\images\train'
val_file_destination = r'd:\ML_Final_Project\yolo_code\yolov7\datasets\images\val'

df = pd.read_csv(mass_csv_path)
image = df['anon_dicom_path']
roi = df['ROI_coords']

preprocess_file_name = os.listdir(preprocess_file_source)

TRAIN_NUM = 5000
VAL_NUM = 618
TOTAL_NUM = TRAIN_NUM + VAL_NUM

count = 0

for i in range(len(image)):
    print(i)
    if (count < TRAIN_NUM): 
        name = image[i][-68:]
        shutil.copyfile(f'{preprocess_file_source}\{name}.png', f'{train_file_destination}\{name}.png')
    elif (count >= TRAIN_NUM and count < TOTAL_NUM):
        name = image[i][-68:]
        shutil.copyfile(f'{preprocess_file_source}\{name}.png', f'{val_file_destination}\{name}.png')
    else:
        break
    count += 1