# Mass Detection-Team28

This project is about to detect the mass in Mammogram images.

If you are not running on a Windows system, please be attentive to all `path-related aspects and command line instructions`, and automatically convert them to the corresponding commands for your system.

* repo name: `ML_Team28`
* suggested env: `Windows`
* used dataset: `EMBED`
* uded preprocess method: `Windowing`, `Bilateral Filter`, `Clahe`, `Canny Algorithm`, `Hough Transform` 
* used model: `CNN`, `YOLOv7`
* overview: 
![overview](https://hackmd.io/_uploads/r1ZXkRXta.png)

If you want to know more about our research detail, please get into the following link!
https://hackmd.io/@MLTeam28/Team28/%2FuEdYu4-ATnmnvHYQS7KVKw

  
- - -

## Setup

You need to `clone our repo first`, and then do the following step to help you finish the Setup.

### Step1 (python dependancy)

You can install all the python dependancy with the below command line instruction.
```
pip install -r /absolute path/to/ML_Team28/requirements.txt
```


### Step2 (node modules)

You can install all the node module needed in running websites with the below command line instruction.

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

* Put theose DICOM image with mass at `path/to/ML_Team28/datasets/image/mass/`
* Put those metadata file at `path/to/ML_Team28/datasets/table/`

We will preprocess all the `DICOM images` located in the `mass` folder and save those `preprocessed PNG image` in the default folder named `mass_png`. 
If you prefer to store the preprocessed PNG images in a custom path, you can add some `additional arguments` provided below.

```
cd path/to/ML_Team28/src/data
python Preprocess.py
```

![image](https://hackmd.io/_uploads/ryN82Z7YT.png)


There are several arguments you can add in command line to help you preprocess efficiently.
* `--mass_matadata_path`:　the path to your metadata
* `--mass_dcm_path`: the path to your DICOM image
* `--mass_png_path`: the path to your PNG image
* `--mass_preprocess_png_path`: the path to your preprocessed PNG image
* `--output_mtable_path`: the path to your updated metadata

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
To convey our project's capabilities, we have designed a website to showcase all of our work. 
You can run the below command line instruction to make the websites work.
```
cd /path/to/ML_Team28/websites/src
npm run start
cd /path/to/ML_Team28/websites/src/server
python server.py
```
* Demo video: https://drive.google.com/file/d/1Az5T5-SPDoeGkuryn_wII9UXA63eJ90z/view?usp=sharing

- - -

## Contact
You can contat us if you have any question!

model group

data group
