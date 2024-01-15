import cv2
import pydicom
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import pylab as pylab
import numpy as np
import pandas as pd
import os
from tqdm import tqdm
from skimage.feature import canny
from skimage.filters import sobel
from skimage.transform import hough_line, hough_line_peaks
from skimage.draw import polygon

from tags import DCM_tags
from to_8_bit_png import process_dicom, apply_windowing as windowing
import argparse

ROI = 'ROI_coords'
POS = 'ViewPosition'
PADDLE = '0_ViewCodeSequence_0_ViewModifierCodeSequence_CodeMeaning'

# for detecting paddle
threshold_factor = 0.95

#----dicom to png----#
def get_png(dcm_pth, png_pth):

    dicom_image = pydicom.dcmread(dcm_pth)
    if "WindowWidth" not in dicom_image or "WindowCenter" not in dicom_image:
        print('no window prerocess')
    meta = DCM_tags(dicom_image)
    arr = np.array(process_dicom(dicom_image.pixel_array, meta.invert, meta.flipHorz, meta.window_centers[0], meta.window_widths[0], meta.voilut_func), dtype=np.uint8)

    cv2.imwrite(png_pth, arr)
    
    return arr

def detect_paddle_shape(image):

    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:

        perimeter = cv2.arcLength(contour, True)

        epsilon = 0.04 * perimeter
        approx = cv2.approxPolyDP(contour, epsilon, True)

        vertices = len(approx)

        # 頂點為4
        if vertices == 4:
            return "Rectangle"
        # 頂點大於8
        elif vertices > 8:
            return "Circle"
    # 沒有符合條件
    return "Unknown"        
        
def fix_table(metadata, isFlip):
    coords = []
    
    #print(clean_metadata.loc[row, ROI])
    if(isFlip):
        return metadata, 'error'
    else:
        for row in range(metadata.shape[0]):
            coords = []
            for c in eval(metadata.loc[row, ROI]):
            #print(c)
                try:
                    coord = (int(c[0]), int(c[1]), int(c[2]), int(c[3]))
            # tuple還有tuple or lsit
                except TypeError:
                    print(row, 'type', c)
                    for c_1 in c:
                        coord = (int(c_1[0]), int(c_1[1]), int(c_1[2]), int(c_1[3]))
                        coords.append(tuple(coord))
            # 逗號後面接()
                except IndexError:
                    print(row, "index" ,c)
                    if c == '()':
                        continue
                    else:
                        try:
                            for c_2 in c:
                                coord = (int(c_2[0]), int(c_2[1]), int(c_2[2]), int(c_2[3]))
                                coords.append(tuple(coord))
                        except:
                            for c_3 in c_2:
                                coord = (int(c_3[0]), int(c_3[1]), int(c_3[2]), int(c_3[3]))
                                coords.append(tuple(coord))
                except:
                    print(row, "error", row, c)
                        #pass
                else:
                    coords.append(tuple(coord))
    #print(row ,coords)
            metadata.loc[row, ROI] = str(coords)
    return metadata
    #print(clean_metadata)

def fix_paddle(arr, type):
    paddle_width = 100
    extracted_tissue = arr
    
    if type == 'Spot Compression':
             
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

   
    elif type == 'Magnification':
        
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

def chack_paddle(i, metadata):
    return metadata.loc[i, PADDLE]=='Spot Compression' or metadata.loc[i, PADDLE]=='Magnification', metadata.loc[i, PADDLE]
    
def delete_rows(pname_list, png_path):
    delete_rows = []
    for i, name in enumerate(pname_list):

        img_pth = png_path+name
        try: 
            if cv2.imread(img_pth) is None:
                print(i)
                delete_rows.append(i)
                continue
        except:
            assert 0 < -1, 'wrong png_path'
        
    return delete_rows

def add_window(dname_list, dcm_path):
    window_list = []
    
    for name in dname_list:
        dicom_image = pydicom.dcmread(dcm_path+name)
        if "WindowWidth" not in dicom_image or "WindowCenter" not in dicom_image:
            print('no window')
            window_list.append(())
        else :
            ww = dicom_image['WindowWidth']
            wc = dicom_image['WindowCenter']
            
            ww = float(ww[0]) if ww.VM > 1 else float(ww.value)
            wc = float(wc[0]) if wc.VM > 1 else float(wc.value)
            
            window_list.append((int(ww), int(wc)))
    return window_list
    

def update_tables(metadata, pname_list, png_path, output_table_path):
    
    deleted_rows = delete_rows(pname_list, png_path)
    metadata = fix_table(metadata=metadata, isFlip=False)
    metadata = metadata.drop(deleted_rows)
    
    metadata.to_csv(output_table_path, sep=',', index=False, header=True)

def update_paddles(metadata, pname_list, png_path):

    for i, name in enumerate(pname_list):
        
        png = png_path+name
        
        arr = cv2.imread(png)
        if arr is None:
            continue
            
        withPaddle = chack_paddle(i, metadata)
        
        if withPaddle[0]:
            extracted = fix_paddle(arr, withPaddle[1])
       
            if (extracted == arr).all():
                os.remove(png)
                continue
        
            cv2.imwrite(png, extracted)

#----enhancement----#
def bilateral_filter(ori_path):  
    ori_img = cv2.imread(ori_path, 0)
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

"""
1. table_only: you have table and need to update them to be consistent with image
2. paddle_only: you have png files and need to update them with removing paddles => True; Otherwise => False
3. mass_only: only mass data need to be processed
4. health_only: only health data need to be processed
5. do all: mass->health->paddle->table
"""
def before_preprocess_interface(table_only=False, paddle_only=False, mass_only=True, health_only=False,\
    mass_metadata = [],\
    health_metadata = [],\
    mass_png_path = "..\\..\\datasets\\image\\clean_png\\",\
    health_png_path = "..\\..\\datasets\\image\\miss_png\\",\
    mass_dcm_path = "..\\..\\datasets\\image\\clean\\",\
    health_dcm_path =  "..\\..\\datasets\\image\\miss\\",\
    output_mtable_path = "..\\..\\datasets\\table\\clean_metadata_test.csv",\
    output_htable_path = "..\\..\\datasets\\table\\miss_metadata_test.csv",\
    mass_pname_list = [],\
    mass_dname_list = [],\
    health_pname_list = [],\
    health_dname_list = []
    ):
                
    #----do table_only----#
    
    if table_only is True:
        if mass_only is True:
            update_tables(metadata=mass_metadata, pname_list= mass_pname_list, png_path=mass_png_path, output_table_path=output_mtable_path)
            
        elif health_only is True:
            update_tables(metadata=health_metadata, pname_list= health_pname_list, png_path=health_png_path, output_table_path=output_htable_path)
            
        else:
            update_tables(metadata=mass_metadata, pname_list= mass_pname_list, png_path=mass_png_path, output_table_path=output_mtable_path)
            update_tables(metadata=health_metadata, pname_list= health_pname_list, png_path=health_png_path, output_table_path=output_htable_path)
            
    #----do paddle_only----#
    
    elif paddle_only is True:
        
        if mass_only is True:
            update_paddles(metadata=mass_metadata, pname_list=mass_pname_list, png_path=mass_png_path)
            update_tables(metadata=mass_metadata, pname_list= mass_pname_list, png_path=mass_png_path, output_table_path=output_mtable_path)
            
        elif health_only is True:
            update_paddles(metadata=health_metadata, pname_list=health_pname_list, png_path=health_png_path)
            update_tables(metadata=health_metadata, pname_list= health_pname_list, png_path=health_png_path, output_table_path=output_htable_path)
            
        else:
            update_paddles(metadata=mass_metadata, pname_list=mass_pname_list, png_path=mass_png_path)
            update_paddles(metadata=health_metadata, pname_list=health_pname_list, png_path=health_png_path)
            
            update_tables(metadata=mass_metadata, pname_list= mass_pname_list, png_path=mass_png_path, output_table_path=output_mtable_path)
            update_tables(metadata=health_metadata, pname_list= health_pname_list, png_path=health_png_path, output_table_path=output_htable_path)
            
    #----do dcm to png----#
    
    else:
        if mass_only is True:
            
            for name in tqdm(mass_dname_list):
                dcm_pth = mass_dcm_path+name
                png_pth = mass_png_path+name+'.png'
                print(dcm_pth)
                print(png_pth)
                get_png(dcm_pth=dcm_pth, png_pth=png_pth)
                
            update_paddles(metadata=mass_metadata, pname_list=mass_pname_list, png_path=mass_png_path)
            update_tables(metadata=mass_metadata, pname_list= mass_pname_list, png_path=mass_png_path, output_table_path=output_mtable_path)
           
        elif health_only is True:
            
            for name in health_dname_list:
                dcm_pth = health_dcm_path+name
                png_pth = health_png_path+name+'.png'
                get_png(dcm_pth=dcm_pth, png_pth=png_pth)
                
            update_paddles(metadata=health_metadata, pname_list=health_pname_list, png_path=health_png_path)
            update_tables(metadata=health_metadata, pname_list= health_pname_list, png_path=health_png_path, output_table_path=output_htable_path)
            
        else:
            for name in mass_pname_list:
                dcm_pth = mass_dcm_path+name
                png_pth = mass_png_path+name+'.png'
                get_png(dcm_pth=dcm_pth, png_pth=png_pth)
                
            update_paddles(metadata=mass_metadata, pname_list=mass_pname_list, png_path=mass_png_path)
            update_tables(metadata=mass_metadata, pname_list= mass_pname_list, png_path=mass_png_path, output_table_path=output_mtable_path)
            
            for name in health_pname_list:
                dcm_pth = health_dcm_path+name
                png_pth = health_png_path+name+'.png'
                get_png(dcm_pth, png_pth)
                
            update_paddles(metadata=health_metadata, pname_list=health_pname_list, png_path=health_png_path)
            update_tables(metadata=health_metadata, pname_list= health_pname_list, png_path=health_png_path, output_table_path=output_htable_path)


def preprocess_interface(enhance_only = True, table_only=False, paddle_only=False, mass_only=True, health_only=False,\
    mass_metadata_path = "..\\..\\datasets\\table\\mass_metadata.csv",\
    health_metadata_path = "..\\..\\datasets\\table\\health_metadata.csv",\
    mass_png_path = "..\\..\\datasets\\image\\mass_png\\",\
    health_png_path = "..\\..\\datasets\\image\\health_png_test\\",\
    mass_dcm_path = "..\\..\\datasets\\image\\mass\\",\
    health_dcm_path =  "..\\..\\datasets\\image\\health\\",\
    mass_preprocess_png_path = "..\\..\\datasets\\image\\mass_preprocess_png\\",\
    health_preprocess_png_path = "..\\..\\datasets\\image\\health_preprocess_png\\",\
    output_mtable_path = "..\\..\\datasets\\table\\mass_metadata_test.csv",\
    output_htable_path = "..\\..\\datasets\\table\\health_metadata_test.csv",\
    fname_column = "anon_dicom_path"):
    
    #----check input type----#
    assert type(paddle_only) is bool and type(table_only) is bool and type(mass_only) is bool and type(health_only) is bool, 'wrong bool variables'
    
    #-----read table----#
    mass_metadata = []
    health_metadata = []
    if mass_only is True or health_only is False:
        try:
            mass_metadata = pd.read_csv(mass_metadata_path, dtype=str)
        except:
            assert 0 < -1, 'wrong mass_metadata_path'
    
    if mass_only is False and health_only is True:    
        try:
            health_metadata = pd.read_csv(health_metadata_path, dtype=str)
        except:
            assert 0 < -1, 'wrong miss_metadata_path'
        
    #----get png name----#
    
    mass_pname_list = []
    mass_dname_list = []
    health_pname_list = []
    health_dname_list = []
    if fname_column == 'anon_dicom_path':
        try: 
            if mass_only is True:
                mass_pname_list = list(map(lambda x: x.split('/')[9]+'.png', mass_metadata[fname_column]))
                mass_dname_list = list(map(lambda x: x.split('/')[9], mass_metadata[fname_column]))
            elif health_only is True:
                health_pname_list = list(map(lambda x: x.split('/')[9]+'.png', health_metadata[fname_column]))
                health_dname_list = list(map(lambda x: x.split('/')[9], health_metadata[fname_column]))
            else:
                mass_pname_list = list(map(lambda x: x.split('/')[9]+'.png', mass_metadata[fname_column]))
                mass_dname_list = list(map(lambda x: x.split('/')[9], mass_metadata[fname_column]))
                health_pname_list = list(map(lambda x: x.split('/')[9]+'.png', health_metadata[fname_column]))
                health_dname_list = list(map(lambda x: x.split('/')[9], health_metadata[fname_column]))
        except:
            assert 0 < -1, 'wrong fname_column'
    
    else:
        try:
            if mass_only is True:
                mass_pname_list = list(mass_metadata[fname_column])
            elif health_only is True:
                health_pname_list = list(health_metadata[fname_column])
            else:
                mass_pname_list = list(mass_metadata[fname_column])
                health_pname_list = list(health_metadata[fname_column])
        except:
            assert 0 < -1, 'wrong fname_column'
    
    #----end check----#
    
    if enhance_only is False:
        before_preprocess_interface(table_only=table_only, paddle_only=paddle_only, mass_only=mass_only, health_only=health_only,\
        mass_metadata = mass_metadata,\
        health_metadata = health_metadata,\
        mass_png_path = mass_png_path,\
        health_png_path = health_png_path,\
        mass_dcm_path = mass_dcm_path,\
        health_dcm_path =  health_dcm_path,\
        output_mtable_path = output_mtable_path,\
        output_htable_path = output_htable_path,\
        mass_pname_list = mass_pname_list,\
        mass_dname_list = mass_dname_list,\
        health_pname_list = health_pname_list,\
        health_dname_list = health_dname_list)
        
        if mass_only is True or health_only is False:
            mass_metadata = pd.read_csv(output_mtable_path, dtype=str)
        if mass_only is False and health_only is True:
            health_metadata = pd.read_csv(output_htable_path, dtype=str)
        
    if mass_only is True:
        mass_pname_list = list(map(lambda x: x.split('/')[9]+'.png', mass_metadata[fname_column]))
        mass_pos = list(mass_metadata[POS])
        mass_zip = zip(mass_pname_list, mass_pos)
    elif health_only is True:
        health_pname_list = list(map(lambda x: x.split('/')[9]+'.png', health_metadata[fname_column]))
        health_pos = list(health_metadata[POS])
        health_zip = zip(health_pname_list, health_pos)
    else:
        mass_pname_list = list(map(lambda x: x.split('/')[9]+'.png', mass_metadata[fname_column]))
        mass_pos = list(mass_metadata[POS])
        mass_zip = zip(mass_pname_list, mass_pos)
            
        health_pname_list = list(map(lambda x: x.split('/')[9]+'.png', health_metadata[fname_column]))
        health_pos = list(health_metadata[POS])
        health_zip = zip(health_pname_list, health_pos)
           
        
    if  mass_only is True or health_only is False:
        for name, pos in tqdm(mass_zip):
            ori_path = mass_png_path+name
            new_path = mass_preprocess_png_path+name
            
            print('\nPreprocessing mass data...', name)
            bil_img = bilateral_filter(ori_path)
            if not isinstance(bil_img, np.ndarray):
                print('Already remove')
                continue
            masked_img = select_breast_area(bil_img)
            clahe_img = clahe(masked_img)
            if pos == 'MLO' and name != '1.2.826.0.1.3680043.8.498.70762477675858797757470697309230496157.dcm':
                rows, cols = clahe_img.shape
                roi = clahe_img[:3 * rows//4, :cols//3]
                hough_img = hough(roi, clahe_img)
                window_img = hough_img
            else:
                window_img = clahe_img
                
            cv2.imwrite(new_path, window_img)
            print('continue')
        print('Mass Finish ...')

    if mass_only is False and health_only is True:
        for name, pos in health_zip:
            ori_path = health_png_path+name
            new_path = health_preprocess_png_path+name
            
            print('Preprocessing health data...', name)
            bil_img = bilateral_filter(ori_path)
            if not isinstance(bil_img, np.ndarray):
                print('Already remove')
                continue
            masked_img = select_breast_area(bil_img)
            clahe_img = clahe(masked_img)
            if pos == 'MLO':
                rows, cols = clahe_img.shape
                roi = clahe_img[:2 * rows//3, :cols//3]
                hough_img = hough(roi, clahe_img)
                cv2.imwrite(new_path, hough_img)
                print('continue')
            else:
                cv2.imwrite(new_path, clahe_img)
                print('continue')
          
    print('All Finish !!!!!!!')

def main():
    parser = argparse.ArgumentParser(description="Preprocess Interface")

    # Add command-line arguments
    parser.add_argument("--enhance_only", action="store_true", help="Enable enhance_only")
    parser.add_argument("--table_only", action="store_true", help="Enable table_only")
    parser.add_argument("--paddle_only", action="store_true", help="Enable paddle_only")

    # Add optional arguments with default values
    parser.add_argument("--mass_metadata_path", default="..\\..\\datasets\\table\\mass_metadata.csv", help="Path to mass metadata")
    parser.add_argument("--mass_dcm_path", default="..\\..\\datasets\\image\\mass\\", help="Path to mass PNG images")
    parser.add_argument("--mass_png_path", default="..\\..\\datasets\\image\\mass_png\\", help="Path to mass PNG images")
    parser.add_argument("--mass_preprocess_png_path", default="..\\..\\datasets\\image\\mass_preprocess_png\\", help="Path to mass PNG images")
    parser.add_argument("--output_mtable_path", default="..\\..\\datasets\\table\\mass_metadata_test.csv", help="Path to mass PNG images")
    parser.add_argument("--fname_column", default="anon_dicom_path", help="Path to mass PNG images")
       
    # Add other optional arguments similarly

    args = parser.parse_args()

    # Call your function with the specified arguments
    preprocess_interface(
        enhance_only=args.enhance_only,
        table_only=args.table_only,
        paddle_only=args.paddle_only,
        mass_only=True,
        mass_metadata_path=args.mass_metadata_path,
        mass_dcm_path = args.mass_dcm_path,
        mass_png_path=args.mass_png_path,
        mass_preprocess_png_path = args.mass_preprocess_png_path,
        output_mtable_path = args.output_mtable_path,
        fname_column = args.fname_column
        # Pass other arguments similarly
    )

if __name__ == "__main__":
    main()