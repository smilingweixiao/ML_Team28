from flask import Flask, jsonify, request, render_template
from preprocess import preprocess_interface as pi
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

# Define your directory path for saving files
UPLOAD_FOLDER = 'path_to_save_files'

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

    if isinstance(handle_list, np.ndarray):
        handle_list = handle_list.tolist()
    if isinstance(png, np.ndarray):
        png = png.tolist()
        
    return jsonify({'png': png, 'view_pos': view_pos, 'paddle': paddle, 'handle_list': handle_list})

if __name__ == '__main__':
    app.run(debug=True)
