from flask import Flask, request, url_for, send_from_directory, jsonify
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Configure the directory where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ... Other routes and setup ...
number = 1


@app.route('/')
def showInfo():
    return "hello, image to Url converter is live"


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    uploaded_file = request.files['file']

    if uploaded_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the uploaded file to the upload directory
    global number
    file_extension = os.path.splitext(uploaded_file.filename)[1]
    fileName = "image"+str(number)+file_extension
    number += 1
    file_path = os.path.join(
        app.config['UPLOAD_FOLDER'], fileName)
    uploaded_file.save(file_path)

    # Construct the URL to the uploaded file based on host name
    host_name = request.host  # Get the host name from the request
    file_url = f'http://{host_name}/{UPLOAD_FOLDER}/{fileName}'

    return jsonify({'file_url': file_url})

# Serve uploaded files


@app.route('/uploads/<filename>')
def serve_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
