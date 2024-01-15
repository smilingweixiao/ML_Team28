# Mass Detection-Team28

If you are not running on a Windows system, please be attentive to all `path-related aspects and command line instructions`, and automatically convert them to the corresponding commands for your system.

* repo name: `ML_Team28`
* suggested env: `Windows`
  
- - -

## Setup

### Step1 (python dependance)
brief description

```
pip install -r /absolute path/to/ML_Team28/requirements.txt
```


### Step2 (node modules)
brief description

```
cd /path/to/ML_Team28/websites/src
npm install
```

### Step3 (get trained weights)
Follow the below link to get TWO weights trained (CNN's and YOLO's) for our application.You should put these TWO at `path/to/ML_Team28/websites/src/server`

If you want to use your own trained weight, you can skip this step.

https://drive.google.com/drive/folders/1vUawesFi8gmUp9oZKanCDosFeXifsr_i?usp=sharing

### Step4 (get dataset)
You should follow the below link to get dataset (EMBED)

https://registry.opendata.aws/emory-breast-imaging-dataset-embed/

- - -

## Preprocess(optional)
```
You can skip this step if you only want to run the application with our trained weights.
```
brief description

* Put theose DICOM image with mass at `path/to/ML_Team28/datasets/image/mass`
* Put those metadata file at `path/to/ML_Team28/datasets/table`

```
cd path/to/ML_Team28/src/data
python Preprocess.py
```

![image](https://hackmd.io/_uploads/ryN82Z7YT.png)


There are several arguments you can add in command line to help you preprocess efficiently.
* enhance_only
* table_only
* paddle_only
* mass_matadata_path
* mass_dcm_path
* mass_png_path
* mass_preprocess_png_path
* output_mtable_path
* fname_column

- - -

## Training Model(optional)
```
You can skip this step if you only want to run the application with our trained weights.
```
brief description
### YOLO
李秉綸

### CNN
王品舜

- - -

## Run application
brief description
```
cd /path/to/ML_Team28/websites/src
npm run start
cd /path/to/ML_Team28/websites/src/server
python server.py
```
* Demo video: https://drive.google.com/file/d/1Az5T5-SPDoeGkuryn_wII9UXA63eJ90z/view?usp=sharing