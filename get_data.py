import pydicom
import numpy as np
import csv
from tags import DCM_tags
from to_8_bit_png import process_dicom, apply_windowing

# for test heres
dcm_pth = r"C:\Users\y9109\Desktop\nthu\junior1\ml\project\embed\image\yes\1.2.826.0.1.3680043.8.498.10000118454892828674141713285403927285.dcm"

dicom_image = pydicom.dcmread(dcm_pth)
meta = DCM_tags(dicom_image)
arr = np.array(process_dicom(dicom_image.pixel_array, meta.invert, meta.flipHorz, meta.window_centers[0], meta.window_widths[0], meta.voilut_func), dtype=np.uint8)

# for test here
#csv_file_path = r"C:\Users\y9109\Desktop\nthu\junior1\ml\project\embed\code\test.csv"
#with open(csv_file_path, 'w', newline='') as csv_file:
#    writer = csv.writer(csv_file)
#    writer.writerow(['output'])
#    for a in arr:
#        writer.writerow([a])