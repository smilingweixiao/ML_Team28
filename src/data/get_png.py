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
min_radius = 50
max_radius = 300

# modify the routes if needs
miss_table_path = "..\\..\\datasets\\table\\miss_metadata.csv"
clean_table_path = "..\\..\\datasets\\table\\clean_metadata_fixed.csv"
miss_png_path = "..\\..\\datasets\\image\\miss_png\\"
clean_png_path = "..\\..\\datasets\\image\\clean_png\\"
miss_path = "..\\..\\datasets\\image\\miss\\"
clean_path = "..\\..\\datasets\\image\\clean\\"

clean_table_path_fixed = "..\\..\\datasets\\table\\clean_metadata_fixed.csv"

miss_metadata = pd.read_csv(miss_table_path, dtype=str)
clean_metadata = pd.read_csv(clean_table_path, dtype=str)

miss_dicoms = list(map(lambda x: x.split('/')[9], pd.read_csv(miss_table_path, dtype=str)['anon_dicom_path']))
clean_dicoms = list(map(lambda x: x.split('/')[9], pd.read_csv(clean_table_path, dtype=str)['anon_dicom_path']))

def get_png(dcm_pth, png_pth, i, isClean):
    #for test
    #print('img#: ', i)
    #withPaddle = ChackPaddle(i, isClean)
    #if not withPaddle[0]:
    #    return
    
    dicom_image = pydicom.dcmread(dcm_pth)
    if "WindowWidth" not in dicom_image or "WindowCenter" not in dicom_image:
        return
    meta = DCM_tags(dicom_image)
    arr = np.array(process_dicom(dicom_image.pixel_array, meta.invert, meta.flipHorz, meta.window_centers[0], meta.window_widths[0], meta.voilut_func), dtype=np.uint8)
    
    #withPaddle = ChackPaddle(i, isClean)
    
    #if withPaddle[0]:
    #    extracted = fix_paddle(arr, withPaddle[1])
    #    if (extracted == arr).all():
    #        #only do once
    #        #os.remove(png_pth)
    #        return
        
        # for debug
    #    cv2.imwrite(png_pth, extracted)
        # comment here if you are debugging with paddle
        #cv2.imwrite(png_pth, extracted)
        
        
    #cv2.imwrite(png_pth, arr)
    if(isClean):
        fix_table(i, meta.flipHorz, np.size(arr, 1))      

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
        
def fix_table(row, isFlip, length):
    coords = []
    
    #print(clean_metadata.loc[row, ROI])
    if(isFlip):
        for c in eval(clean_metadata.loc[row, ROI]):
            print(length, c)
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
                        pass
                        
            except:
                print(row, "error", row, c)
                # pass
            else:
                coords.append(tuple(coord))
    else:
        for c in eval(clean_metadata.loc[row, ROI]):
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
    clean_metadata.loc[row, ROI] = str(coords)
    
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
        
        shape = detect_paddle_shape(binary_img)
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
        print('sucess', paddle_top, paddle_bottom)

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
        
        shape = detect_paddle_shape(binary_img)
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
        print('sucess', paddle_top, paddle_bottom)

        #cv2.imshow('img1', arr)
        #cv2.waitKey(0)
        #cv2.imshow('img2', extracted_tissue)
        #cv2.waitKey(0)
        
        #cv2.destroyAllWindows()
        
    return extracted_tissue


def ChackPaddle(i, isClean):
    if isClean:
        return clean_metadata.loc[i, PADDLE]=='Spot Compression' or clean_metadata.loc[i, PADDLE]=='Magnification', clean_metadata.loc[i, PADDLE]
    else:
        return miss_metadata.loc[i, PADDLE]=='Spot Compression' or miss_metadata.loc[i, PADDLE]=='Magnification', miss_metadata.loc[i, PADDLE]

    

#uncomment here if you are ready
#for i, name in enumerate(miss_dicoms):
#    dcm_pth = miss_path+name
#    png_pth = miss_png_path+name+".png"
#    get_png(dcm_pth, png_pth, i, isClean=False)
    
#for i, name in enumerate(clean_dicoms):
#    fix_table(i, False, 0)
    #print(i)
    #dcm_pth = clean_path+name
    #png_pth = clean_png_path+name+".png"
    #get_png(dcm_pth, png_pth, i, isClean=True)
    
    #break
    
delete_rows = []
for i, name in enumerate(clean_dicoms):
    #print(i)
    
    png_pth = clean_png_path+name+".png"
    if cv2.imread(png_pth) is None:
        print(i)
        delete_rows.append(i)
        continue
    fix_table(i, False, 0)
        
clean_metadata = clean_metadata.drop(delete_rows)

    
clean_metadata.to_csv(clean_table_path_fixed, sep=',', index=False, header=True)
    
