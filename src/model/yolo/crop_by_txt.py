"""
This python script will crop images by given text file, checking if images exist.
You can use this to crop images of YOLO's output coordinates, checking the performance of YOLO.
File not found mweans YOLO detect nothing in the file.
"""

import pandas as pd
import cv2
import os


mass_csv_path = r'd:\ML_Final_Project\ml\ML_Team28\datasets\table\clean_metadata_fixed.csv'
train_yolo_label_path = r'D:\ML_Final_Project\yolo_code\yolov7\datasets\labels\CNN_labels_010'
train_yolo_image_path = r'D:\ML_Final_Project\ml\ML_Team28\datasets\image\clean_preprocess_png'
val_yolo_label_path = r'.\datasets\labels\val'
val_yolo_image_path = r'D:\ML_Final_Project\ml\ML_Team28\datasets\image\clean_preprocess_png'
crop_img_path = r"D:\ML_Final_Project\yolo_code\yolov7\datasets\images\crop_png_3"

df = pd.read_csv(mass_csv_path)
image = df['anon_dicom_path']
mass_num = df['num_roi']
roi = df['ROI_coords']

TRAIN_NUM = 5000
VAL_NUM = 684
TOTAL_NUM = TRAIN_NUM + VAL_NUM

filenames = os.listdir(train_yolo_label_path)
print(filenames)

file = 0
# i-th image
for i in range(len(image)):
    if (i == TOTAL_NUM): break
    if (i < TRAIN_NUM): 
        image_path = train_yolo_image_path
    else: 
        image_path = val_yolo_image_path

    name = image[i][-68:]
    # print(name)
    try: 
        with open(f'{train_yolo_label_path}\{name}.txt', 'r') as f:
            for nums, j in enumerate(f.readlines()):
                j = j.split(' ')
                j[-1] = j[-1][:-1]
                ymin = int(float(j[0]))
                xmin = int(float(j[1]))
                ymax = int(float(j[2]))
                xmax = int(float(j[3]))
                img = cv2.imread(f'{image_path}\{name}.png')
                crop_img = img[ymin:ymax, xmin:xmax]
                # print(i + 2, f'{image_path}\{name}.png', w, h)
                print(i + 2, ymin, xmin, ymax, xmax)
                if (nums > 0):
                    output_path = crop_img_path + f'\{name}({nums}).png'
                else: 
                    output_path = crop_img_path + f'\{name}.png'
                # print(f'\{name}.png')
                # print(output_path)
                cv2.imwrite(output_path, crop_img)
    except FileNotFoundError:
        file += 1
        print('file not found')
    except: 
        print('unknown error')
print(f'{file} file not found')