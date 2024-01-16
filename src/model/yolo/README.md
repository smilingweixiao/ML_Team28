# YOLO README

**In this section you can train your own YOLO by files we provided and original YOLOv7's Github repo**

### Given files explanation
* Yolo has its own format of labels, you can run *labels.py* python script to generate labels given by metadata.
* After training, if you want to convert YOLO's txt output file into csv, you can run *label_to_csv.py* python scripy.
* If you want to check YOLO's performance or ground truth image, you can run *crop_by_csv.py* and *crop_by_txt.py* to crop ROIs.
* If lots of files need to transfer between directory, we also provide *move_file.py* for your convenience.
* Model's config file of YOLO is *yolov7-mammo.yaml*.
* Data's config file of YOLO is *mammo.yaml*.
* parameter is in *hyp.mammo.yaml*.

### Training Preparation
* Clone YOLOv7 Github repo in another folder.
* Change working directory into YOLO's folder.
* Move *yolov7-mammo.yaml* into YOLO_folder\cfg\training.
* Move *mammo.yaml* into YOLO_folder\data.
* Move *hyp.mammo.yaml* into YOLO_folder\data.
* Create datasets, datasets\images, datasets\labels, datasets\images\train, datasets\images\val, datasets\labels\train, datasets\labels\val folders under YOLO's folder.
* Move preprocessed images into YOLO_folder\datasets\images\train and YOLO_folder\datasets\images\val, you can use *move_file.py*.
* Read the documentation string and modify file path in *labels.py*.
* Run "labels.py* to generate labels and file list for YOLO.

### Start Training
Run below command, don't forget to check path, the weight can be obtain in YOLOv7's Github repo.
```
python .\train.py --weights .\weights\yolov7_training.pt  --cfg .\cfg\training\yolov7-mammo.yaml --hyp .\data\hyp.mammo.yaml --data .\data\mammo.yaml --batch-size x --epoch x --device x --img-size 640 --save_period x --adam
```

### Training with CNN
After training complete, we can generate training data for CNN. The command below will generate txt files for each images.
```
python .\detect.py --weights .\runs\train\exp\weights\best.pt --source .\datasets\images\val\ --conf-thres x --save-txt --save-conf
```
Then you will need to run *label_to_csv.py* to generate csv file for CNN's training.

### Start Inferencing
You can run the same command as above to predict
```
python .\detect.py --weights .\runs\train\exp\weights\best.pt --source .\datasets\images\val\ --conf-thres x --save-txt --save-conf
```

**Please note that YOLO is preliminary mass detector in our work**