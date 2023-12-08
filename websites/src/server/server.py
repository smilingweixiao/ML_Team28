from flask import Flask, jsonify, request, render_template
from preprocess_interface import preprocess_interface as pi

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api', methods=['POST'])
def get_data():
    
    json_data = request.get_json()

    dicom = json_data.get('dicom', '')
    view_pos = json_data.get('view_pos', '')
    paddle = json_data.get('paddle', '')
    
    png, view_pos, paddle, handle_list = pi(dicom=dicom, view_pos=view_pos, paddle=paddle)


    return jsonify({'png': png, 'view_pos':view_pos, 'paddle':paddle, 'handle_list': handle_list})

if __name__ == '__main__':
    app.run(debug=True)
