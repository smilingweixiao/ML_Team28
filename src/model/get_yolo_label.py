import pandas as pd

mass_csv_path = r'..\..\table\clean_metadata.csv'
yolo_label_path = r'.\yolov7\datasets\labels\train'


df = pd.read_csv(mass_csv_path)
image = df['anon_dicom_path']
mass_num = df['num_roi']
roi = df['ROI_coords']

# i-th image
for i in range(len(image)):
    name = image[i][-68:]
    with open(f'{yolo_label_path}\{name}.txt', 'w') as f:
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