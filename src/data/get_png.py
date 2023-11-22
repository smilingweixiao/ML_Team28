import pydicom
import cv2
import numpy as np
import pandas as pd
import csv
from tags import DCM_tags
from to_8_bit_png import process_dicom, apply_windowing

# for test heres
#dcm_pth = r"..\image\clean\1.2.826.0.1.3680043.8.498.10000118454892828674141713285403927285.dcm"
ROI = 'ROI_coords'

# modify the routes if needs
miss_table_path = "..\\..\\datasets\\table\\miss_metadata.csv"
clean_table_path = "..\\..\\datasets\\table\\clean_metadata.csv"
miss_png_path = "..\\..\\datasets\\image\\miss_png\\"
clean_png_path = "..\\..\\datasets\\image\\clean_png\\"
miss_path = "..\\..\\datasets\\image\\miss\\"
clean_path = "..\\..\\datasets\\image\\clean\\"

clean_table_path_fixed = "..\\..\\table\\clean_metadata_fixed.csv"

clean_metadata = pd.read_csv(clean_table_path, dtype=str)

miss_dicoms = list(map(lambda x: x.split('/')[9], pd.read_csv(miss_table_path, dtype=str)['anon_dicom_path']))
clean_dicoms = list(map(lambda x: x.split('/')[9], pd.read_csv(clean_table_path, dtype=str)['anon_dicom_path']))

def get_png(dcm_pth, png_pth, i, isClean):

    dicom_image = pydicom.dcmread(dcm_pth)
    if "WindowWidth" not in dicom_image or "WindowCenter" not in dicom_image:
        return
    meta = DCM_tags(dicom_image)
    arr = np.array(process_dicom(dicom_image.pixel_array, meta.invert, meta.flipHorz, meta.window_centers[0], meta.window_widths[0], meta.voilut_func), dtype=np.uint8)
    cv2.imwrite(png_pth, arr)
    if(isClean):
        fix_table(i, meta.flipHorz, np.size(arr, 1)) 
        
        
        
def fix_table(row, isFlip, length):
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
                coord = (c[0], c[1], c[2], c[3])
            # tuple還有tuple or lsit
            except TypeError:
                print(row, 'type', c)
                for c_1 in c:
                    coord = (c_1[0], c_1[1], c_1[2], c_1[3])
                    coords.append(tuple(coord))
            # 逗號後面接()
            except IndexError:
                print(row, "index" ,c)
                if c == '()':
                    pass
                else:
                    try:
                        for c_2 in c:
                            coord = (c_2[0], c_2[1], c_2[2], c_2[3])
                            coords.append(tuple(coord))
                    except:
                        pass
            except:
                print(row, "error", row, c)
                #pass
            else:
                coords.append(tuple(coord))
    #print(row ,coords)
    clean_metadata.loc[row, ROI] = str(coords)
    
    #print(clean_metadata)
    
#uncomment here if you are ready
#for i, name in enumerate(miss_dicoms):
#    dcm_pth = miss_path+name
#    png_pth = miss_png_path+name+".png"
#    get_png(dcm_pth, png_pth, i, isClean=False)
    
for i, name in enumerate(clean_dicoms):
    dcm_pth = clean_path+name
    png_pth = clean_png_path+name+".png"
    get_png(dcm_pth, png_pth, i, isClean=True)
    #break
    
clean_metadata.to_csv(clean_table_path_fixed, sep=',', index=False, header=True)
    


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