# YOLO README

**In this section you can train your own YOLO by files we provided and original YOLOv7's Github repo**

### Training preparation
* Yolo has its own format of labels, you can run *labels.py* python script to generate labels given by metadata.
* After training, if you want to convert YOLO's txt output file into csv, you can run *label_to_csv.py* python scripy.
* If you want to check YOLO's performance or ground truth image, you can run *crop_by_csv.py* and *crop_by_txt.py* to crop ROIs.
* If lots of files need to transfer between directory, we also provide *move_file.py* for your convenience.
* Model's config file of YOLO is *yolov7-mammo.yaml*.
* Data's config file of YOLO is *mammo.yaml*.

### Start Training
You can run below command, don't forget to check path.
```
python .\train.py --weights .\weights\yolov7_training.pt  --cfg .\cfg\training\yolov7-mammo.yaml --data .\data\mammo.yaml --batch-size x --epoch x --device x --img-size 640 --save_period x --adam
```

**Please note that YOLO is preliminary mass detector in our work**