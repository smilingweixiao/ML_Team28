import pandas as pd
import csv
p
patient_id="empi_anon"
RANDOM_SEED=1
TOTAL_ROW=20000

metadata = pd.read_csv("D:\\tables\EMBED_OpenData_metadata.csv", dtype=str)
clinical = pd.read_csv("D:\\tables\EMBED_OpenData_clinical.csv", dtype=str)
selected_metadata_path = "E:\\ml\\table\\clean_metadata.csv"
selected_clinical_path = "E:\\ml\\table\\clean_clinical.csv"
miss_metadata_path = "E:\\ml\\table\\miss_metadata.csv"
miss_clinical_path = "E:\\ml\\table\\miss_clinical.csv"


all_clean_metadata = metadata[metadata['ROI_coords']!='()'].to_dict(orient='records')
all_dirty_metadata = metadata[metadata['ROI_coords']=='()'] 
all_clean_clinical = clinical[clinical['massshape'].notna()] 
all_dirty_clinical = clinical[clinical['massshape'].isnull()]

clean_metadata = []
clean_clinical = pd.DataFrame()

dirty_metadata = []
dirty_clinical = pd.DataFrame()

id = -1
for e in all_clean_metadata:
    if id == int(e[patient_id]):
        clean_metadata.append(e)
        continue
    
    c = all_clean_clinical[all_clean_clinical[patient_id]==e[patient_id]]
    if not c.empty :
        clean_metadata.append(e)
        id = int(e[patient_id])
        clean_clinical = pd.concat([clean_clinical, c])

print(len(clean_metadata))
clean_metadata = pd.DataFrame.from_records(clean_metadata)

id=-1
random_dirty_metadata = all_dirty_metadata.sample(n=TOTAL_ROW, random_state=RANDOM_SEED).to_dict(orient='records')

for e in random_dirty_metadata:
    if id == int(e[patient_id]):
        dirty_metadata.append(e)
        continue
    
    c = all_dirty_clinical[all_dirty_clinical[patient_id]==e[patient_id]]
    if not c.empty :
        dirty_metadata.append(e)
        id = int(e[patient_id])
        dirty_clinical = pd.concat([dirty_clinical, c])

print(len(dirty_metadata))
dirty_metadata = pd.DataFrame.from_records(dirty_metadata)


clean_metadata.to_csv(selected_metadata_path, sep=',', index=True, header=True)
clean_clinical.to_csv(selected_clinical_path, sep=',', index=True, header=True)
dirty_metadata.to_csv(miss_metadata_path, sep=',', index=True, header=True)
dirty_clinical.to_csv(miss_clinical_path, sep=',', index=True, header=True)
