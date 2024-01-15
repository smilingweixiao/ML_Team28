"""
This python script will generate YOLO's format label by given metadata.
coordinate in metadate be like: y1, x1, y2, x2
"""

import pandas as pd
import cv2

mass_csv_path = r'd:\ML_Final_Project\ml\ML_Team28\datasets\table\clean_metadata_fixed.csv'
train_yolo_label_path = r'.\datasets\labels\train'
train_yolo_image_path = r'.\datasets\images\train'
val_yolo_label_path = r'.\datasets\labels\val'
val_yolo_image_path = r'.\datasets\images\val'

df = pd.read_csv(mass_csv_path)
image = df['anon_dicom_path']
mass_num = df['num_roi']
roi = df['ROI_coords']

TRAIN_NUM = 1000
VAL_NUM = 200
TOTAL_NUM = TRAIN_NUM + VAL_NUM

# i-th image
for i in range(len(image)):
    if (i == TOTAL_NUM): break
    if (i < TRAIN_NUM): 
        label_path = train_yolo_label_path
        image_path = train_yolo_image_path
    else: 
        label_path = val_yolo_label_path
        image_path = val_yolo_image_path

    name = image[i][-68:]
    with open(f'{label_path}\{name}.txt', 'w') as f:
        # there's j-th roi in i-th image
        output = eval(roi[i])
        print(output)
        for j in output:
            ymin = int(j[0])
            xmin = int(j[1])
            ymax = int(j[2])
            xmax = int(j[3])
            w = cv2.imread(f'{image_path}\{name}.png').shape[1]
            h = cv2.imread(f'{image_path}\{name}.png').shape[0]
            # print(i + 2, f'{image_path}\{name}.png', w, h)
            print(i + 2, ymin, xmin, ymax, xmax)
            f.write(f'0 {(xmin + xmax) / (2 * w)} {(ymin + ymax) / (2 * h)} {(xmax - xmin) / w} {(ymax - ymin) / h}\n')