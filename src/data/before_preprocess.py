# run this before you run preprocess.ipynb !!!

import pydicom
import cv2
import numpy as np
import pandas as pd
import csv
import os
from tags import DCM_tags
from to_8_bit_png import process_dicom, apply_windowing

# for test heres
#dcm_pth = r"..\image\clean\1.2.826.0.1.3680043.8.498.10000118454892828674141713285403927285.dcm"
ROI = 'ROI_coords'
PADDLE = '0_ViewCodeSequence_0_ViewModifierCodeSequence_CodeMeaning'

# for detecting paddle
threshold_factor = 0.95
#min_radius = 50
#max_radius = 300

# modify the routes if needs
#miss_table_path = "..\\..\\datasets\\table\\miss_metadata.csv"
#clean_table_path = "..\\..\\datasets\\table\\clean_metadata.csv"
#miss_png_path = "..\\..\\datasets\\image\\miss_png\\"
#clean_png_path = "..\\..\\datasets\\image\\clean_png\\"
#miss_path = "..\\..\\datasets\\image\\miss\\"
#clean_path = "..\\..\\datasets\\image\\clean\\"
#
#clean_table_path_fixed = "..\\..\\datasets\\table\\clean_metadata_fixed.csv"
#
#miss_metadata = pd.read_csv(miss_table_path, dtype=str)
#clean_metadata = pd.read_csv(clean_table_path, dtype=str)
#
#miss_pname_list = list(map(lambda x: x.split('/')[9], pd.read_csv(miss_table_path, dtype=str)['anon_dicom_path']))
#clean_pname_list = list(map(lambda x: x.split('/')[9], pd.read_csv(clean_table_path, dtype=str)['anon_dicom_path']))

def get_png(dcm_pth, png_pth):
    #for test
    #print('img#: ', i)
    #withPaddle = ChackPaddle(i, isClean)
    #if not withPaddle[0]:
    #    return None
    
    dicom_image = pydicom.dcmread(dcm_pth)
    if "WindowWidth" not in dicom_image or "WindowCenter" not in dicom_image:
        print('no window prerocess')
    meta = DCM_tags(dicom_image)
    arr = np.array(process_dicom(dicom_image.pixel_array, meta.invert, meta.flipHorz, meta.window_centers[0], meta.window_widths[0], meta.voilut_func), dtype=np.uint8)

    cv2.imwrite(png_pth, arr)
    
    return arr

def detect_paddle_shape(image):
    # 灰度化
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #_, binary = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)

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
        for c in eval(clean_metadata.loc[row, ROI]):
            #print(c)
            try:
                coord = (c[0], (length-int(c[3])), c[2], (length-int(c[1])))
            # tuple還有tuple or lsit
            except TypeError:
                print(row, "type", c)
                for c_1 in c:
                    coord = (c_1[0], (length-int(c_1[3])), c_1[2], (length-int(c_1[1])))
                    coords.append(tuple(coord))
            # 逗號後面接() or list with list
            except IndexError:
                print(row, "index" ,c)
                if c == '()':
                    pass
                else:
                    try:
                        for c_2 in c:
                            coord = (c_2[0], (length-int(c_2[3])), c_2[2], (length-int(c_2[1])))
                            coords.append(tuple(coord))
                    except:
                        for c_3 in c_2:
                            coord = (int(c_3[0]), int(c_3[1]), int(c_3[2]), int(c_3[3]))
                            coords.append(tuple(coord))
                        
            except:
                print(row, "error", row, c)
                # pass
            else:
                coords.append(tuple(coord))
    else:
        for row in range(metadata.shape[0]):
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
                        pass
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
    
    #cv2.namedWindow('img1', cv2.WINDOW_NORMAL)
    #cv2.namedWindow('img2', cv2.WINDOW_NORMAL)
    #cv2.namedWindow('img_error', cv2.WINDOW_NORMAL)
    
    if type == 'Spot Compression':
        
        #if shape != "Rectangle":
        #    cv2.imshow('img_error', arr)
        #    cv2.waitKey(0)
        #    print(shape)
        #    return
        
        hist, _ = np.histogram(arr.flatten(), bins=256, range=[0, 256])
        
        peak_intensity = np.argmax(hist)
        
        threshold_value = int(peak_intensity * threshold_factor)
        
        _, binary_img = cv2.threshold(arr, threshold_value, 255, cv2.THRESH_BINARY)
        
        #shape = detect_paddle_shape(binary_img)
        #if shape != "Rectangle":
        #    print(shape)
        #    cv2.imshow('img_error', arr)
        #    cv2.waitKey(0)
        #    return extracted_tissue
        
        row_sums = np.sum(binary_img, axis=1)
        #
        row_sums[0:500] = 0
        row_sums[len(row_sums)-250:len(row_sums)] = 0
        #
        paddle_top = np.argmax(row_sums)
        row_sums[paddle_top-paddle_width:paddle_top+paddle_width] = 0
        paddle_bottom = len(row_sums) - np.argmax(np.flip(row_sums))
        
        if paddle_top+paddle_width>=paddle_bottom-paddle_width or paddle_bottom-paddle_top < 400:
            #cv2.imshow('img_error', arr)
            #cv2.waitKey(0)
            print(paddle_top, paddle_bottom)
            return arr
        
        mask = arr.copy()
        mask[:,:] = 0
        mask[paddle_top+paddle_width:paddle_bottom-paddle_width, :] = 255
        
        extracted_tissue = arr.copy()
        extracted_tissue[mask == 0] = 0
        extracted_tissue[mask != 0] = arr[mask != 0]
        print('success', paddle_top, paddle_bottom)

        #cv2.imshow('img1', arr)
        #cv2.waitKey(0)
        #cv2.imshow('img2', extracted_tissue)
        #cv2.waitKey(0)
        
        #cv2.destroyAllWindows()
   
    elif type == 'Magnification':
        #paddle_width = 300
        #if shape != "Rectangle":
        #    cv2.imshow('img_error', arr)
        #    cv2.waitKey(0)
        #    print(shape)
        #    return
        
        hist, _ = np.histogram(arr.flatten(), bins=256, range=[0, 256])
        
        peak_intensity = np.argmax(hist)
        
        threshold_value = int(peak_intensity * threshold_factor)
        
        _, binary_img = cv2.threshold(arr, threshold_value, 255, cv2.THRESH_BINARY)
        
        #shape = detect_paddle_shape(binary_img)
        #if shape != "Rectangle":
        #    print(shape)
        #    cv2.imshow('img_error', arr)
        #    cv2.waitKey(0)
        #    cv2.destroyAllWindows()
        #    return extracted_tissue
        
        row_sums = np.sum(binary_img, axis=1)
        
        paddle_top = np.argmax(row_sums)
        row_sums[paddle_top-paddle_width:paddle_top+paddle_width] = 0
        paddle_bottom = len(row_sums) - np.argmax(np.flip(row_sums))
        
        if paddle_top > len(row_sums)/4 or paddle_bottom < len(row_sums)-len(row_sums)/4:
            return arr
        
        if paddle_top+paddle_width>=paddle_bottom-paddle_width or paddle_bottom-paddle_top < 400:
            #cv2.imshow('img_error', arr)
            #cv2.waitKey(0)
            print(paddle_top, paddle_bottom)
            return arr
        
        mask = arr.copy()
        mask[:,:] = 0
        mask[paddle_top+paddle_width:paddle_bottom-paddle_width, :] = 255
        
        extracted_tissue = arr.copy()
        extracted_tissue[mask == 0] = 0
        extracted_tissue[mask != 0] = arr[mask != 0]
        print('success', paddle_top, paddle_bottom)

        #cv2.imshow('img1', arr)
        #cv2.waitKey(0)
        #cv2.imshow('img2', extracted_tissue)
        #cv2.waitKey(0)
        
        #cv2.destroyAllWindows()
        
    return extracted_tissue


def ChackPaddle(i, metadata):
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
        

def update_tables(metadata, pname_list, png_path, output_table_path):
    
    #if mass_only:
    deleted_rows = delete_rows(pname_list, png_path)
    metadata = fix_table(metadata, False)
    metadata = metadata.drop(deleted_rows)
    metadata.to_csv(output_table_path, sep=',', index=False, header=True)


def update_paddles(metadata, pname_list, png_path):

    for i, name in enumerate(pname_list):
        
        png = png_path+name
        
        arr = cv2.imread(png)
        if arr is None:
            continue
            
        withPaddle = ChackPaddle(i, metadata)
        
        if withPaddle[0]:
            extracted = fix_paddle(arr, withPaddle[1])
       
            if (extracted == arr).all():
                os.remove(png)
                continue
        
            cv2.imwrite(png, extracted)

"""
1. table_only: you have table and need to update them to be consistent with image
2. paddle_only: you have png files and need to update them with removing paddles => True; Otherwise => False
3. mass_only: only mass data need to be processed
4. health_only: only health data need to be processed
5. do all: mass->health->paddle->table
"""
def before_preprocess(table_only=False, paddle_only=False, mass_only=True, health_only=False,\
    mass_metadata_path = "..\\..\\datasets\\table\\clean_metadata_test.csv",\
    health_metadata_path = "..\\..\\datasets\\table\\miss_metadata.csv",\
    mass_png_path = "..\\..\\datasets\\image\\clean_png_test\\",\
    health_png_path = "..\\..\\datasets\\image\\miss_png\\",\
    mass_dcm_path = "..\\..\\datasets\\image\\clean\\",\
    health_dcm_path =  "..\\..\\datasets\\image\\miss\\",\
    output_mtable_path = "..\\..\\datasets\\table\\clean_metadata_test.csv",\
    output_htable_path = "..\\..\\datasets\\table\\miss_metadata_fixed.csv",\
    fname_column = "anon_dicom_path"):
    
    #----check input type----#
    #assert type(paddle_only) is bool
    assert type(paddle_only) is bool and type(table_only) is bool and type(mass_only) is bool and type(health_only) is bool, 'wrong bool variables'
    
    #-----read table----#
    try:
        health_metadata = pd.read_csv(health_metadata_path, dtype=str)
    except:
        assert 0 < -1, 'wrong miss_metadata_path'
        
    try:
        mass_metadata = pd.read_csv(mass_metadata_path, dtype=str)
    except:
        assert 0 < -1, 'wrong mass_metadata_path'
        
        
    #----get png name----#
    
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
            update_tables(metadata=health_metadata, name_list= health_pname_list, png_path=health_png_path, output_table_path=output_htable_path)
            
        else:
            update_paddles(metadata=mass_metadata, pname_list=mass_pname_list, png_path=mass_png_path)
            update_paddles(metadata=health_metadata, pname_list=health_pname_list, png_path=health_png_path)
            
            update_tables(metadata=mass_metadata, pname_list= mass_pname_list, png_path=mass_png_path, output_table_path=output_mtable_path)
            update_tables(metadata=health_metadata, pname_list= health_pname_list, png_path=health_png_path, output_table_path=output_htable_path)
            
    #----do dcm to png----#
    
    else:
        if mass_only is True:
            
            for name in mass_dname_list:
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

 

#before_preprocess(paddle_only=True)
    
