import pandas as pd
import shutil

img_path_from_prefix = "D:\\images\\cohort_"
selected_img_path_to_prefix = "E:\\ml\\image\\clean"
miss_img_path_to_prefix = "E:\\ml\\image\\miss"

selected_metadata_path = "E:\\ml\\table\\clean_metadata.csv"
miss_metadata_path = "E:\\ml\\table\\miss_metadata.csv"

#metadata = pd.read_csv(selected_metadata_path, dtype=str)
#metadata_d = metadata.to_dict(orient='records')
#for i, e in enumerate(metadata_d):
#    linux_addr = str(e['anon_dicom_path']).split('_',4)[2].split('/')
#    addr = (linux_addr[0]+'\\'+linux_addr[1]+'\\'+linux_addr[2]+'\\'+linux_addr[3]+'\\'+linux_addr[4])
#    #print(addr)
#    fr = img_path_from_prefix+addr
#    to = selected_img_path_to_prefix+'\\'+linux_addr[4]
#    #print(to)
#    shutil.copyfile(fr, to)

metadata = pd.read_csv(miss_metadata_path, dtype=str)
metadata_d = metadata.to_dict(orient='records')
for i, e in enumerate(metadata_d):
    linux_addr = str(e['anon_dicom_path']).split('_',4)[2].split('/')
    addr = (linux_addr[0]+'\\'+linux_addr[1]+'\\'+linux_addr[2]+'\\'+linux_addr[3]+'\\'+linux_addr[4])
    #print(addr)
    fr = img_path_from_prefix+addr
    to = miss_img_path_to_prefix+'\\'+linux_addr[4]
    #print(to)
    shutil.copyfile(fr, to)
