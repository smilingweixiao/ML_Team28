"""
This python script can turn YOLO's format label to a single csv file, you can run this to generate training data for CNN.
"""

import pandas as pd
import cv2

output = pd.DataFrame()
NAME = []
ROI = []

# csv path
mass_csv_path = r'd:\ML_Final_Project\ml\ML_Team28\datasets\table\clean_metadata_fixed.csv'

train_yolo_label_path = r'.\runs\detect\labels_005_exp49_test\labels'
val_yolo_label_path = r'.\runs\detect\exp4\labels'

train_yolo_image_path = r'.\datasets\images\val'
val_yolo_image_path = r'.\datasets\images\val'

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
        label_path = train_yolo_label_path
        image_path = train_yolo_image_path
    else: 
        label_path = val_yolo_label_path
        image_path = val_yolo_image_path
    name = image[i][-68:]
    img = cv2.imread(f'{image_path}\{name}.png')
    try:
        with open(f'{label_path}\{name}.txt', 'r') as f:
            NAME.append(name)
            temp = []
            # with open(f'{output_label_path}\{name}.txt', 'w') as f2:
            for j in f.readlines():
                w = img.shape[1]
                h = img.shape[0]
                j = j.split(' ')[1:]
                j[-1] = j[-1][:-1]
                # print(j)
                x_center, y_center, yolo_w, yolo_h, conf = j
                x_center, y_center, yolo_w, yolo_h = float(x_center), float(y_center), float(yolo_w), float(yolo_h)
                print(x_center, y_center, yolo_w, yolo_h, conf)
                xmin = (x_center * 2 * w - yolo_w * w) / 2
                xmax = (x_center * 2 * w + yolo_w * w) / 2
                ymin = (y_center * 2 * h - yolo_h * h) / 2
                ymax = (y_center * 2 * h + yolo_h * h) / 2
                temp.append((ymin, xmin, ymax, xmax, float(conf)))
            ROI.append(temp)
    except FileNotFoundError:
        no_mass_count += 1
        NAME.append(name)
        ROI.append([])
        print(name)
        print(r"There's no mass detected in this img")
    except:
        print('unknown Error')
print(f"total {no_mass_count} img didn't detect mass")
output['name'] = NAME
output['ROI'] = ROI
output.to_csv('CNN_labels_005_exp49_test.csv', index = False)