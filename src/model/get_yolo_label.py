import pandas as pd

mass_csv_path = r'd:\ML_Final_Project\ml\ML_Team28\datasets\table\clean_metadata.csv'
train_yolo_label_path = r'.\datasets\labels\train'
val_yolo_label_path = r'.\datasets\labels\val'

df = pd.read_csv(mass_csv_path)
image = df['anon_dicom_path']
mass_num = df['num_roi']
roi = df['ROI_coords']

TRAIN_NUM = 1000
VAL_NUM = 200
TOTAL_NUM = TRAIN_NUM + VAL_NUM

# i-th image
for i in range(len(image)):
    if (i == TOTAL_NUM): break
    if (i < TRAIN_NUM): path = train_yolo_label_path
    else: path = val_yolo_label_path

    name = image[i][-68:]
    with open(f'{path}\{name}.txt', 'w') as f:
        # there's j-th roi in i-th image
        temp = roi[i][1:-1]
        output = []
        length = len(temp.split('), '))
        for j, k in enumerate(temp.split('), ')):
            if (j == length - 1):
                output.append(k[1:-1].split(', '))
            else:
                output.append(k[1:].split(', '))
            if (length == 1 and j == 0):
                output[0][3] = output[0][3][:-1]
        for j in output:
            if (j[0] == ""): continue
            ymin = int(j[0])
            xmin = int(j[1])
            ymax = int(j[2])
            xmax = int(j[3])
            w = xmax - xmin
            h = ymax - ymin
            print(i + 2, ymin, xmin, ymax, xmax)
            f.write(f'0 {(xmin + xmax) / (2 * w)} {(ymin + ymax) / (2 * h)} {(xmax - xmin) / w} {(ymax - ymin) / h}\n')
