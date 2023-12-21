import cv2
import pandas as pd
import os
import numpy as np

# csv path
mass_csv_path = r'd:\ML_Final_Project\ml\ML_Team28\datasets\table\clean_metadata_fixed.csv'
# wherer to generate labels
train_yolo_label_path = r'.\runs\detect\exp3\labels'
val_yolo_label_path = r'.\runs\detect\exp2\labels'
# where's the png
train_yolo_image_path = r'.\datasets\images\train'
val_yolo_image_path = r'.\datasets\images\val'

output_label_path = r'd:\ML_Final_Project\yolo_code\yolov7\datasets\labels\CNN_labels_train'

df = pd.read_csv(mass_csv_path)
image = df['anon_dicom_path']
roi = df['ROI_coords']

TRAIN_NUM = 5000
VAL_NUM = 618
TOTAL_NUM = TRAIN_NUM + VAL_NUM

# i-th image
no_mass_count = 0
for i in range(len(image)):
    if (i == TOTAL_NUM): break
    if (i < TRAIN_NUM): 
        # continue
        label_path = train_yolo_label_path
        image_path = train_yolo_image_path
    else: 
        continue
        label_path = val_yolo_label_path
        image_path = val_yolo_image_path
    name = image[i][-68:]
    img = cv2.imread(f'{image_path}\{name}.png')
    try:
        with open(f'{label_path}\{name}.txt', 'r') as f:
            with open(f'{output_label_path}\{name}.txt', 'w') as f2:
                for j in f.readlines():
                    w = img.shape[1]
                    h = img.shape[0]
                    j = j.split(' ')[1:]
                    j[-1] = j[-1][:-1]
                    # print(j)
                    x_center, y_center, yolo_w, yolo_h = j
                    x_center, y_center, yolo_w, yolo_h = float(x_center), float(y_center), float(yolo_w), float(yolo_h)
                    print(x_center, y_center, yolo_w, yolo_h)
                    xmin = (x_center * 2 * w - yolo_w * w) / 2
                    xmax = (x_center * 2 * w + yolo_w * w) / 2
                    ymin = (y_center * 2 * h - yolo_h * h) / 2
                    ymax = (y_center * 2 * h + yolo_h * h) / 2
                    # x y w h
                    # f2.write(f'{xmin} {ymin} {xmax - xmin} {ymax - ymin}\n')
                    # y1 x1 y2 x2
                    f2.write(f'{ymin} {xmin} {ymax} {xmax}\n')
    except FileNotFoundError:
        no_mass_count += 1
        print(name)
        print(r"There's no mass detected in this img")
    except:
        print('unknown Error')
print(f"total {no_mass_count} img didn't detect mass")