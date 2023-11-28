import pydicom
import cv2
import numpy as np
import pandas as pd
import csv
from matplotlib import pyplot as plt
from tags import DCM_tags
from to_8_bit_png import process_dicom, apply_windowing


# for test heres
#dcm_pth = r"..\image\clean\1.2.826.0.1.3680043.8.498.10000118454892828674141713285403927285.dcm"

# modify the routes if needs
miss_table_path = "..\\..\\table\\miss_metadata.csv"
clean_table_path = "..\\..\\table\\clean_metadata.csv"
miss_png_path = "..\\..\\image\\miss_png\\"
clean_png_path = "..\\..\\image\\clean_png\\"
miss_path = "..\\..\\image\\miss\\"
clean_path = "..\\..\\image\\clean\\"

miss_dicoms = list(map(lambda x: x.split('/')[9], pd.read_csv(miss_table_path, dtype=str)['anon_dicom_path']))
clean_dicoms = list(map(lambda x: x.split('/')[9], pd.read_csv(clean_table_path, dtype=str)['anon_dicom_path']))

def get_png(dcm_pth, png_pth):

    dicom_image = pydicom.dcmread(dcm_pth)
    if "WindowWidth" not in dicom_image or "WindowCenter" not in dicom_image:
        return
    meta = DCM_tags(dicom_image)
    arr = np.array(process_dicom(dicom_image.pixel_array, meta.invert, meta.flipHorz, meta.window_centers[0], meta.window_widths[0], meta.voilut_func), dtype=np.uint8)
    #plt.hist(arr.flatten(), bins=100, range=(1, 255))
    #plt.show()
    cv2.imwrite(png_pth, arr)
    
#uncomment here if you are ready
#for name in miss_dicoms:
#    dcm_pth = miss_path+name
#    png_pth = miss_png_path+name+".png"
#    get_png(dcm_pth, png_pth)
    
for name in clean_dicoms:
    dcm_pth = clean_path+name
    png_pth = clean_png_path+name+".png"
    get_png(dcm_pth, png_pth)
    print("get png")
    img = cv2.imread(clean_png_path+name+".png",0)
    plt.imshow(img, cmap='gray')
    plt.show()
    print("start hist")
    equ = cv2.equalizeHist(img)
    clahe = cv2.createCLAHE(clipLimit =2.0, tileGridSize=(8,8))
    cl_img = clahe.apply(img)
    plt.imshow(cl_img, cmap='gray')

    #plt.axis('off')
    plt.show()
    
    #plt.hist(img.flat, bins=100, range=(0, 255))
    #print("break")
    break
    


## for test here
#cv2.imwrite('before.jpg', dicom_image.pixel_array.astype(np.uint8))
#cv2.imwrite('after.jpg', arr)
#s = cv2.imread('after.jpg')
#cv2.imshow('img', s)
#cv2.waitKey(0)

#csv_file_path = r"test.csv"
#with open(csv_file_path, 'w', newline='') as csv_file:
#    writer = csv.writer(csv_file)
#    writer.writerow(['output'])
#    for a in arr:
#        writer.writerow(a)