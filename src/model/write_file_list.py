import os

train_filename = []
val_filename = []
train_png_dir_path = r'./datasets/image/train/'
val_png_dir_path = r'./datasets/image/val/'
train_list_file = r'./datasets/train_list.txt'
val_list_file = r'./datasets/val_list.txt'

# train
train_filename = os.listdir(train_png_dir_path)
with open(train_list_file, 'w') as f:
    for i in train_filename:
        f.write(f'datasets/images/train/{i}\n')

# val
val_filename = os.listdir(val_png_dir_path)
with open(val_list_file, 'w') as f:
    for i in val_filename:
        f.write(f'datasets/images/val/{i}\n')