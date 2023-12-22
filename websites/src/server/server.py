from preprocess import preprocess_interface as pi
from detect import yolo_detection as yolo
from flask import Flask, jsonify, request, render_template, make_response
from werkzeug.utils import secure_filename
import os
import cv2
from PIL import Image
from flask_cors import CORS
import numpy as np
import base64


app = Flask(__name__)
CORS(app)
#CORS(app, resources={r"/*": {"origins": "http://localhost:9000"}})

# Define your directory path for saving files
UPLOAD_FOLDER = 'path_to_save_files'
DOWNLOAD_PNG = '.\\preprocessed\\preprocessed.png'
#DOWNLOAD_PNG = '.\\preprocessed\\1.2.826.0.1.3680043.8.498.69071597029523690507650697989983609866.dcm.png'

YOLO_IMG = '.\\runs\\detect\\exp\\preprocessed.png'
YOLO_LABEL = '.\\runs\\detect\\exp\\labels\\preprocessed.txt'
#YOLO_IMG = '.\\runs\\detect\\exp\\1.2.826.0.1.3680043.8.498.69071597029523690507650697989983609866.dcm.png'


# Create the directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/', methods=['POST'])
def get_data():
    # Ensure 'dicom' file is part of the request
    if 'dicom' not in request.files:
        return jsonify({'error': 'No dicom file part'}), 400

    dicom_file = request.files['dicom']
    filename = secure_filename(dicom_file.filename)

    # Use the UPLOAD_FOLDER path
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    dicom_file.save(file_path)

    view_pos = request.form.get('view_pos', '')
    paddle = request.form.get('paddle', '')

    # Process the file with your preprocess_interface function
    png, view_pos, paddle, handle_list = pi(dicom_path=file_path, view_pos=view_pos, paddle=paddle)
    #
    ##upload the png
    #dest_path = os.path.join(UPLOAD_FOLDER, PNG_NAME)
    #image_to_save = Image.fromarray(png.encode('utf-8').decode('base64'))
    #image_to_save.save(dest_path)

    if isinstance(handle_list, np.ndarray):
        handle_list = handle_list.tolist()
    if isinstance(png, np.ndarray):
        png = png.tolist()
        
    return jsonify({'png': png, 'view_pos': view_pos, 'paddle': paddle, 'handle_list': handle_list})

@app.route('/api/detect/', methods=['POST'])
def yolo_detect():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:9000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    
    #png_file = Image.open(DOWNLOAD_PNG)
    print('DOING YOLOOOOOOOO')
    yolo(source=DOWNLOAD_PNG)
    
    buffer = cv2.imread(YOLO_IMG)
    #png = base64.b64encode(buffer).decode('utf-8')
    _, buffer_en = cv2.imencode('.png', buffer)
    png = base64.b64encode(buffer_en).decode('utf-8')
    
    with open(YOLO_LABEL, 'r') as f:
        labels = []
        w = buffer.shape[1]
        h = buffer.shape[0]
        
        for label in f.readlines():
            #labels.append(label.split())
            label = label.split(' ')
            x_center, y_center, yolo_w, yolo_h, conf =\
            float(label[0]), float(label[1]), float(label[2]), float(label[3]), float(label[4])
            dct = {'xmin': (x_center * 2 * w - yolo_w * w) / 2, \
                   'xmax': (x_center * 2 * w + yolo_w * w) / 2, \
                   'ymin': (y_center * 2 * h - yolo_h * h) / 2, \
                   'ymax': (y_center * 2 * h + yolo_h * h) / 2, \
                   'confidence': conf}
            labels.append(dct)                   
            

    
    print('label = ', labels)
    
    
    if isinstance(png, np.ndarray):
        png = png.tolist()
        
       
    return jsonify({'png': png, 'labels': labels})

@app.route('/api/detect/', methods=['POST'])
def crop_png():
    return
if __name__ == '__main__':
    app.run(debug=True)
