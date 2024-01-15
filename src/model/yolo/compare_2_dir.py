"""
This python script will compare files in 2 different directory, you can run this to check if labels match images
"""
import os

dir1 = r'd:\ML_Final_Project\yolo_code\yolov7\datasets\images\train'
dir2 = r'd:\ML_Final_Project\yolo_code\yolov7\datasets\labels\train'

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
if (flag): print("the same!")