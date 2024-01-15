"""
This python script integrate the training preparation in our paper.
1. Read in coordinate given by metadata.
2. Remove duplicate ground truth ROIs.
3. Remove ROIs that is entirely black
4. Remove super large ROIs
5. Comppare labels and Images to check matching.
6. Write YOLO's labels list into directory.

This file require following data:
1. Csv file of metadata -> mass_csv_path
2. Path to generate lebels -> train_yolo_label_path, val_yolo_label_path
3. Path pf preprocessed images -> train_yolo_image_path, val_yolo_image_path
4. Traing data number -> TRAIN_NUM
5. Validation data number -> VAL_NUM
6. Threshold to determine whether ROIs is the same -> IOU_THRESHOLD
"""

import numpy as np
import pandas as pd
import cv2
import os


# csv path
mass_csv_path = r'.\datasets\table\clean_metadata_test.csv'
# wherer to generate labels
train_yolo_label_path = r'.\datasets\labels\train'
val_yolo_label_path = r'.\datasets\labels\val'
# where's the png
train_yolo_image_path = r'.\datasets\images\train'
val_yolo_image_path = r'.\datasets\images\val'

df = pd.read_csv(mass_csv_path)
image = df['anon_dicom_path']
roi = df['ROI_coords']

TRAIN_NUM = 5000
VAL_NUM = 618
TOTAL_NUM = TRAIN_NUM + VAL_NUM
IOU_THRESHOLD = 0.1

# i-th image
black_count, large_count, same_count = 0, 0, 0
for i in range(len(image)):
    if (i == TOTAL_NUM): break
    if (i < TRAIN_NUM): 
        label_path = train_yolo_label_path
        image_path = train_yolo_image_path
    else: 
        label_path = val_yolo_label_path
        image_path = val_yolo_image_path

    name = image[i][-68:]
    img = cv2.imread(f'{image_path}\{name}.png')
    with open(f'{label_path}\{name}.txt', 'w') as f:
        # there's j-th roi in i-th image
        output = list(eval(roi[i]))
        # remove same ROI by calculating IOU
        remove = []
        for m in range(len(output)):
            for n in range(m + 1, len(output)):
                x1 = max(output[m][1], output[n][1])
                y1 = max(output[m][0], output[n][0])
                x2 = min(output[m][3], output[n][3])
                y2 = min(output[m][2], output[n][2])
                intersecA = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)
                # Calculate areas of individual boxes
                box1_area = (output[m][2] - output[m][0] + 1) * (output[m][3] - output[m][1] + 1)
                box2_area = (output[n][2] - output[n][0] + 1) * (output[n][3] - output[n][1] + 1)
                # Calculate Union area
                union_area = box1_area + box2_area - intersecA
                # Calculate IoU
                iou = intersecA / union_area
                if (iou > IOU_THRESHOLD):
                    same_count += 1
                    print(f'same ROI, {name}')
                    if (box1_area > box2_area): remove.append(m)
                    else: remove.append(n)
        remove = list(set(remove))
        remove.sort()
        for j in remove[::-1]:
            output.pop(j)
        # get ROI, convert to YOLO format
        for j in output:
            ymin = int(j[0])
            xmin = int(j[1])
            ymax = int(j[2])
            xmax = int(j[3])
            crop_img = img[ymin:ymax, xmin:xmax]
            w = img.shape[1]
            h = img.shape[0]
            # print(i + 2, f'{image_path}\{name}.png', w, h)
            print(i + 2, ymin, xmin, ymax, xmax)
            # check if ROI is black or too large
            if (np.all(crop_img == 0)): 
                print(f'remove black ROI, {name}')
                black_count += 1
                continue
            if ((xmax - xmin) * (ymax - ymin) >= 1000 * 1000):
                print(f'remove super large ROI, {name}')
                large_count += 1
                continue
            f.write(f'0 {(xmin + xmax) / (2 * w)} {(ymin + ymax) / (2 * h)} {(xmax - xmin) / w} {(ymax - ymin) / h}\n')
print(f'\nthere are {black_count} black ROI, {large_count} super large ROI, {same_count} same ROI')
print(f'total remove {black_count + large_count + same_count} ROI')

# ---------- compare 2 dir ----------

# train
dir1 = train_yolo_image_path
dir2 = train_yolo_label_path
content1 = os.listdir(dir1)
content2 = os.listdir(dir2)
flag = 1
if (len(content1) != len(content2)): 
    flag = 0
    print("not the same")
else: 
    for i in range(len(content1)):
        if (content1[i][:-4] != content2[i][:-4]):
            print("not the same")
            flag = 0
            break
if (flag): print("train labels the same!")

# val
dir3 = val_yolo_image_path
dir4 = val_yolo_label_path
content3 = os.listdir(dir3)
content4 = os.listdir(dir4)
flag = 1
if (len(content3) != len(content4)): 
    flag = 0
    print("not the same")
else: 
    for i in range(len(content3)):
        if (content3[i][:-4] != content4[i][:-4]):
            print("not the same")
            flag = 0
            break
if (flag): print("val labels the same!")

# ---------- write file list ----------

train_filename = []
val_filename = []
train_png_dir_path = train_yolo_image_path
val_png_dir_path = val_yolo_image_path
train_list_file = r'.\datasets\train_list.txt'
val_list_file = r'.\val_list.txt'

# train
train_filename = os.listdir(train_png_dir_path)
with open(train_list_file, 'w') as f:
    for i in train_filename:
        f.write(f'datasets/images/train/{i}\n')

# val
val_filename = os.listdir(val_png_dir_path)
with open(val_list_file, 'w') as f:
    for i in val_filename:
        f.write(f'datasets/images/val/{i}\n')