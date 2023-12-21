from preprocess import preprocess_interface as pi
from yolo.detect import yolo_detection as yolo
from flask import Flask, jsonify, request, render_template
from crop_png import crop_png as cp
from werkzeug.utils import secure_filename
import os
import cv2
from PIL import Image
from flask_cors import CORS
import numpy as np
import base64

app = Flask(__name__)
CORS(app)

# Define your directory path for saving files
UPLOAD_FOLDER = 'path_to_save_files'
DOWNLOAD_PNG = '.\\preprocessed\\preprocessed.png'

YOLO_IMG = 'yolo\\runs\\detect\\exp\\preprocessed.png'

# Create the directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api', methods=['POST'])
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

@app.route('/yolo', methods=['POST'])
def crop_data():
    
    #png_file = Image.open(DOWNLOAD_PNG)
    
    yolo(source=DOWNLOAD_PNG)
    buffer = cv2.imread(YOLO_IMG)
    png = base64.b64encode(buffer).decode('utf-8')

    if isinstance(png, np.ndarray):
        png = png.tolist()
        
    return jsonify({'png': png})

if __name__ == '__main__':
    app.run(debug=True)
