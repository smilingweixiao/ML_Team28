"""
This python script will crop images by given metadata attribute and output to selected folder.
You can run this to check ground truth ROIs.
"""
import pandas as pd
import cv2

mass_csv_path = r'd:\ML_Final_Project\ml\ML_Team28\datasets\table\clean_metadata_test.csv'
train_yolo_label_path = r'.\datasets\labels\train'
train_yolo_image_path = r'D:\ML_Final_Project\ml\ML_Team28\datasets\image\clean_preprocess_png_test'
val_yolo_label_path = r'.\datasets\labels\val'
val_yolo_image_path = r'D:\ML_Final_Project\ml\ML_Team28\datasets\image\clean_preprocess_png_test'
crop_img_path = r"D:\ML_Final_Project\yolo_code\yolov7\datasets\images\crop_png_test"

df = pd.read_csv(mass_csv_path)
image = df['anon_dicom_path']
mass_num = df['num_roi']
roi = df['ROI_coords']

TRAIN_NUM = 5000
VAL_NUM = 618
TOTAL_NUM = TRAIN_NUM + VAL_NUM

# i-th image
for i in range(len(image)):
    if (i == TOTAL_NUM): break
    if (i < TRAIN_NUM): 
        image_path = train_yolo_image_path
    else: 
        image_path = val_yolo_image_path

    name = image[i][-68:]
    # there's j-th roi in i-th image
    output = eval(roi[i])
    for nums, j in enumerate(output):
        ymin = int(j[0])
        xmin = int(j[1])
        ymax = int(j[2])
        xmax = int(j[3])
        img = cv2.imread(f'{image_path}\{name}.png')
        w = img.shape[1]
        h = img.shape[0]
        crop_img = img[ymin:ymax, xmin:xmax]
        print(i + 2, ymin, xmin, ymax, xmax)
        if (nums > 0):
            output_path = crop_img_path + f'\{name}({nums}).png'
        else: 
            output_path = crop_img_path + f'\{name}.png'
        cv2.imwrite(output_path, crop_img)
