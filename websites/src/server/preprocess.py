import cv2
import os
import pydicom
import base64
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas as pd
from skimage.feature import canny
from skimage.filters import sobel
from skimage.transform import hough_line, hough_line_peaks
from skimage.draw import polygon
from matplotlib import pylab as pylab

from tags import DCM_tags
from to_8_bit_png import process_dicom, apply_windowing

def bilateral_filter(ori_img):  
    #ori_img = cv2.imread(ori_path, 0)
    # print(ori_path,'to', bil_path)
    if ori_img is not None:
        bil_img = cv2.bilateralFilter(ori_img, 9, 150, 150)
        return bil_img
    else:
        return False

def select_breast_area(bil_img):
    # binarization: use thresholding to create a binary mask
    th, img_binary = cv2.threshold(bil_img, 7, 255, cv2.THRESH_BINARY)
    # expand the border of white contours (dliate -> open)
    kernel = np.ones((21,21),np.uint8)
    img_opening = cv2.morphologyEx(img_binary, cv2.MORPH_OPEN, kernel)
    # deciding the breast area with binary mask
    img_masked = cv2.bitwise_and(bil_img,img_opening)
    return img_masked

def clahe(img):
    equ = cv2.equalizeHist(img)
    clahe = cv2.createCLAHE(clipLimit =3.0, tileGridSize=(4,4))
    cl_img = clahe.apply(img)
    ret, thresh3 = cv2.threshold(cl_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return cl_img

def apply_canny(image):
    # img = cv2.medianBlur(image, 9)                 # 模糊化，去除雜訊
    output = cv2.Canny(image, 10, 35) 
    return output

def get_hough_lines(canny_img):
    h, theta, d = hough_line(canny_img)
    lines = list()
    # print('\nAll hough lines')
    for _, angle, dist in zip(*hough_line_peaks(h, theta, d)):
        # print("Angle: {:.2f}, Dist: {:.2f}".format(np.degrees(angle), dist))
        x1 = 0
        y1 = (dist - x1 * np.cos(angle)) / np.sin(angle + 0.0001)
        x2 = canny_img.shape[1]
        y2 = (dist - x2 * np.cos(angle)) / np.sin(angle + 0.0001)
        lines.append({
            'dist': dist,
            'angle': np.degrees(angle),
            'point1': [x1, y1],
            'point2': [x2, y2]
        })
    
    return lines

def shortlist_lines(lines):
    MIN_ANGLE = 20
    MAX_ANGLE = 90
    MIN_DIST  = 100
    MAX_DIST  = 1300
    
    shortlisted_lines = [x for x in lines if 
                          (x['dist']>=MIN_DIST) &
                          (x['dist']<=MAX_DIST) &
                          (x['angle']>=MIN_ANGLE) &
                          (x['angle']<=MAX_ANGLE)
                        ]
    # print('\nShorlisted lines')
    # for i in shortlisted_lines:
    #     print("Angle: {:.2f}, Dist: {:.2f}".format(i['angle'], i['dist']))
        
    return shortlisted_lines

def remove_pectoral(shortlisted_lines):
    shortlisted_lines.sort(key = lambda x: x['dist'])
    # print(shortlisted_lines)
    pectoral_line = shortlisted_lines[0]
    d = pectoral_line['dist']
    theta = np.radians(pectoral_line['angle'])
    
    x_intercept = d/np.cos(theta)
    y_intercept = d/np.sin(theta)
    
    return polygon([0, 0, y_intercept], [0, x_intercept, 0])

def hough(image, cla_image):
    rows, cols = image.shape

    # Step 2: Contour detection using Canny filter
    img = cv2.medianBlur(image, 33)  
    canny_image = apply_canny(img)

    # Step 3: Linear aperture filtering
    filtered_image = cv2.filter2D(canny_image, -1, np.array([[0, 2, 0], [2, 2, 2], [0, 2, 0]]))

    # Step 4: Line detection using Hough Transform
    lines = get_hough_lines(filtered_image)
    shortlisted_lines = shortlist_lines(lines)
    
    # Step 5: Apply the Hough mask to the region of interest
    if len(shortlisted_lines) > 0:
        rr, cc = remove_pectoral(shortlisted_lines)
        # Create a boolean mask for the conditions
        mask = (rr < rows) & (cc < cols)
        # Set values to 0 where the conditions are met
        cla_image[rr[mask], cc[mask]] = 0
        return cla_image
    else:
        return cla_image


def fix_paddle(arr, type):
    paddle_width = 100
    threshold_factor = 0.95
    extracted_tissue = arr
    
    if type == 'spot compression':
        
        
        hist, _ = np.histogram(arr.flatten(), bins=256, range=[0, 256])
        
        peak_intensity = np.argmax(hist)
        
        threshold_value = int(peak_intensity * threshold_factor)
        
        _, binary_img = cv2.threshold(arr, threshold_value, 255, cv2.THRESH_BINARY)
     
        row_sums = np.sum(binary_img, axis=1)
        
        row_sums[0:500] = 0
        row_sums[len(row_sums)-250:len(row_sums)] = 0
        
        paddle_top = np.argmax(row_sums)
        row_sums[paddle_top-paddle_width:paddle_top+paddle_width] = 0
        paddle_bottom = len(row_sums) - np.argmax(np.flip(row_sums))
        
        if paddle_top+paddle_width>=paddle_bottom-paddle_width or paddle_bottom-paddle_top < 400:

            print(paddle_top, paddle_bottom)
            return arr
        
        mask = arr.copy()
        mask[:,:] = 0
        mask[paddle_top+paddle_width:paddle_bottom-paddle_width, :] = 255
        
        extracted_tissue = arr.copy()
        extracted_tissue[mask == 0] = 0
        extracted_tissue[mask != 0] = arr[mask != 0]
        print('success', paddle_top, paddle_bottom)

   
    elif type == 'magnification':
        
        hist, _ = np.histogram(arr.flatten(), bins=256, range=[0, 256])
        
        peak_intensity = np.argmax(hist)
        
        threshold_value = int(peak_intensity * threshold_factor)
        
        _, binary_img = cv2.threshold(arr, threshold_value, 255, cv2.THRESH_BINARY)
        
        row_sums = np.sum(binary_img, axis=1)
        
        paddle_top = np.argmax(row_sums)
        row_sums[paddle_top-paddle_width:paddle_top+paddle_width] = 0
        paddle_bottom = len(row_sums) - np.argmax(np.flip(row_sums))
        
        if paddle_top > len(row_sums)/4 or paddle_bottom < len(row_sums)-len(row_sums)/4:
            return arr
        
        if paddle_top+paddle_width>=paddle_bottom-paddle_width or paddle_bottom-paddle_top < 400:
            
            print(paddle_top, paddle_bottom)
            return arr
        
        mask = arr.copy()
        mask[:,:] = 0
        mask[paddle_top+paddle_width:paddle_bottom-paddle_width, :] = 255
        
        extracted_tissue = arr.copy()
        extracted_tissue[mask == 0] = 0
        extracted_tissue[mask != 0] = arr[mask != 0]
        print('success', paddle_top, paddle_bottom)
        
    return extracted_tissue

def before_preprocess_interface(dicom=None, paddle=None, handle_list=[]):
    
    handle_list = []
    
    if "WindowWidth" not in dicom or "WindowCenter" not in dicom:
        print('no window prerocess')
    else:
        handle_list.append('windowing')
        
    meta = DCM_tags(dicom)
    arr = np.array(process_dicom(dicom.pixel_array, meta.invert, meta.flipHorz, meta.window_centers[0], meta.window_widths[0], meta.voilut_func), dtype=np.uint8)
    extract_tissue = arr
    if type(paddle) is str:

        extract_tissue = fix_paddle(arr=arr, type=paddle.lower())
        if not np.array_equal(extract_tissue, arr):
            handle_list.append('paddle')
            print('have paddle')
            
    return extract_tissue, handle_list
    
    
def preprocess_interface(dicom_path=None, view_pos=None, paddle=None):
    
    dicom = pydicom.dcmread(dicom_path)

    if dicom is None:
        return None, view_pos, paddle, None
    handle_list=[]
    
    print('Preprocessing data in Server...')

    ori_img, handle_list = before_preprocess_interface(dicom, paddle, handle_list)
    
    print('do ', handle_list, 'in before_preprocess')
    
    bil_img = bilateral_filter(ori_img)
    #if not isinstance(bil_img, np.ndarray):
    #   print('Already remove')
    #    return None
    masked_img = select_breast_area(bil_img)
    clahe_img = clahe(masked_img)
    
    handle_list.append('bilateral_filter')
    handle_list.append('clahe')
    
    #if type(view_pos) is str and view_pos.upper() == 'MLO'
    if view_pos == "2":
        rows, cols = clahe_img.shape
        roi = clahe_img[:3 * rows//4, :cols//3]
        hough_img = hough(roi, clahe_img)
        #cv2.imwrite(r"C:\Users\y9109\Desktop\nthu\junior1\ml\project\ML_Team28\datasets\image\web_png"+r'\test.png', hough_img)
        handle_list.append('hough')
        print('do ', handle_list, 'in preprocess')
        
        file_path = os.path.join('preprocessed', 'preprocessed.png')
        cv2.imwrite(file_path, hough_img)
        
        _, buffer = cv2.imencode('.png', hough_img)
        png_as_base64 = base64.b64encode(buffer).decode('utf-8')
        #----------------------------------------------
        return png_as_base64, view_pos, paddle, handle_list
        
    else:        #cv2.imwrite(r"C:\Users\y9109\Desktop\nthu\junior1\ml\project\ML_Team28\datasets\image\web_png"+r'\test.png', clahe_img)
        
        
        print('do ', handle_list, 'in preprocess')
        
        file_path = os.path.join('preprocessed', 'preprocessed.png')
        cv2.imwrite(file_path, clahe_img)
        
        _, buffer = cv2.imencode('.png', clahe_img)
        png_as_base64 = base64.b64encode(buffer).decode('utf-8')
        #----------------------------------------------
        return png_as_base64, view_pos, paddle, handle_list
    


# test
#dicom = pydicom.dcmread(r"C:\Users\y9109\Desktop\nthu\junior1\ml\project\ML_Team28\datasets\image\clean\1.2.826.0.1.3680043.8.498.35243124038639653326409267615926837320.dcm")
#preprocess_interface(dicom=dicom, view_pos='mlo')


    
    
    