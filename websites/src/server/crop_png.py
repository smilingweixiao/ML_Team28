import cv2

def crop_png(png_path, crop_path, labels):
    
    img = cv2.imread(png_path)
    
    for i, lab in enumerate(labels, start=1):
        
        crop_img = img[int(lab['ymin']):int(lab['ymax']), int(lab['xmin']):int(lab['xmax'])]
        cv2.imwrite(crop_path + 'crop' +str(i) + '.png', crop_img)