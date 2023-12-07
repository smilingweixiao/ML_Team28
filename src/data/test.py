# ---------- module ----------

import pandas as pd
import cv2
import os

# ---------- get YOLO labels ----------

mass_csv_path = "..\\..\\datasets\\table\\clean_metadata_fixed.csv"
#train_yolo_label_path = r'.\datasets\labels\train'
train_yolo_image_path = r'C:\Users\y9109\Desktop\nthu\junior1\ml\project\ML_Team28\datasets\image\clean_png'
#val_yolo_label_path = r'.\datasets\labels\val'
val_yolo_image_path = r'C:\Users\y9109\Desktop\nthu\junior1\ml\project\ML_Team28\datasets\image\clean_png'
crop_img_path = "..\\..\\datasets\\image\\crop_png"


df = pd.read_csv(mass_csv_path)
image = df['anon_dicom_path']
mass_num = df['num_roi']
roi = df['ROI_coords']

TRAIN_NUM = 1000
VAL_NUM = 200
TOTAL_NUM = TRAIN_NUM + VAL_NUM

# i-th image
print(len(image))
for i in range(len(image)):
    if (i == TOTAL_NUM): break
    if (i < TRAIN_NUM): 
        #label_path = train_yolo_label_path
        image_path = train_yolo_image_path
    else: 
        #label_path = val_yolo_label_path
        image_path = val_yolo_image_path

    name = image[i][-68:]
    #with open(f'{label_path}\{name}.txt', 'w') as f:
        # there's j-th roi in i-th image
    output = eval(roi[i])
    for j in output:
        ymin = int(j[0])
        xmin = int(j[1])
        ymax = int(j[2])
        xmax = int(j[3])
        img = cv2.imread(f'{image_path}\{name}.png')
        try:
            w = img.shape[1]
            h = img.shape[0]
        except:
            continue
        crop_img = img[ymin:ymax, xmin:xmax]
        # print(i + 2, f'{image_path}\{name}.png', w, h)
        print(i + 2, ymin, xmin, ymax, xmax)
        output_path = crop_img_path + f'\{name}.png'
        # print(f'\{name}.png')
        # print(output_path)
        cv2.imwrite(output_path, crop_img)
        # f.write(f'0 {(xmin + xmax) / (2 * w)} {(ymin + ymax) / (2 * h)} {(xmax - xmin) / w} {(ymax - ymin) / h}\n')