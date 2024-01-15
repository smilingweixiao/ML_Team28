import os
import cv2
import numpy as np

crop_img_path = r"D:\ML_Final_Project\yolo_code\yolov7\datasets\images\crop_png"
clean_png_path = r"d:\ML_Final_Project\yolo_code\yolov7\datasets\images\train"
label_path = r"d:\ML_Final_Project\yolo_code\yolov7\datasets\labels\train"

count = 0
for i, filename in enumerate(os.listdir(crop_img_path)):
    img_path = os.path.join(crop_img_path, filename)
    crop_img = cv2.imread(img_path)
    if(np.all(crop_img == 0)):
        print("remove one image")
        os.remove(f'{clean_png_path}\{filename}')
        os.remove(f'{label_path}\{filename[:-8]}.dcm.txt')
        count += 1