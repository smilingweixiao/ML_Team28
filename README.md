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

Link to the two weights:
* [resnext_newyolo__checkpoint_best.pth](https://drive.google.com/file/d/1VnspBLDTcL7WnQpr-E_XSGatJUH1uEJr/view?usp=sharing)
* [best.pt](https://drive.google.com/file/d/12cE0a1t9MGOFEy4CsU-KIlxJ5fcBe2tJ/view?usp=sharing)

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

Notify: Training YOLO will takes you a long time, we strongly suggest you to use the provided weights.

#### Given files explanation
* Yolo has its own format of labels, you can run *labels.py* python script to generate labels given by metadata.
* After training, if you want to convert YOLO's txt output file into csv, you can run *label_to_csv.py* python scripy.
* If you want to check YOLO's performance or ground truth image, you can run *crop_by_csv.py* and *crop_by_txt.py* to crop ROIs.
* If lots of files need to transfer between directory, we also provide *move_file.py* for your convenience.
* Model's config file of YOLO is *yolov7-mammo.yaml*.
* Data's config file of YOLO is *mammo.yaml*.
* parameter is in *hyp.mammo.yaml*.

#### Training Preparation
* Clone YOLOv7 Github repo in another folder.
* Change working directory into YOLO's folder.
* Move *yolov7-mammo.yaml* into YOLO_folder\cfg\training.
* Move *mammo.yaml* into YOLO_folder\data.
* Move *hyp.mammo.yaml* into YOLO_folder\data.
* Create datasets, datasets\images, datasets\labels, datasets\images\train, datasets\images\val, datasets\labels\train, datasets\labels\val folders under YOLO's folder.
* Move preprocessed images into YOLO_folder\datasets\images\train and YOLO_folder\datasets\images\val, you can use *move_file.py*.
* Read the documentation string and modify file path in *labels.py*.
* Run "labels.py* to generate labels and file list for YOLO.

#### Start Training
Run below command, don't forget to check path, the weight can be obtain in YOLOv7's Github repo.
```
python .\train.py --weights .\weights\yolov7_training.pt  --cfg .\cfg\training\yolov7-mammo.yaml --hyp .\data\hyp.mammo.yaml --data .\data\mammo.yaml --batch-size x --epoch x --device x --img-size 640 --save_period x --adam
```
#### Training with CNN
After training complete, we can generate training data for CNN. The command below will generate txt files for each images.
```
python .\detect.py --weights .\runs\train\exp\weights\best.pt --source .\datasets\images\val\ --conf-thres x --save-txt --save-conf
```
Then you will need to run *label_to_csv.py* to generate csv file for CNN's training.

#### Start Inferencing
You can run the same command as above to predict
```
python .\detect.py --weights .\runs\train\exp\weights\best.pt --source .\datasets\images\val\ --conf-thres x --save-txt --save-conf
```


### CNN

Notify: Training CNN will takes you a long time, we strongly suggest you to use the provided weights.

#### Get weight you need in training CNN

Please download the weight in the following link, and store it at `/path/to/ML_Team28/src/model/cnn/`

[convnext_tf3_newyolo__checkpoint_best.pth](https://drive.google.com/file/d/1n07pL9wDpqSX_Fl4URyBZgI9eYnVcKSn/view?usp=sharing)


#### Structure
1. CNN model training
2. CNN model evaluation
3. Yolo+CNN evaluation

#### Start training

If you want to train your own CNN weights, please check the file`/path/to/ML_Team28/src/model/cnn/CNN_model_training_and_evaluation.ipynb`, and follow the instruction in that notebook to finish your training.



- - -

## Run Application
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

Welcom to contat us if you have any question!

