from flask import Flask, jsonify, render_template, send_from_directory, request
from flask_cors import CORS

import os

app = Flask(__name__, template_folder='templates')
CORS(app)

UPLOAD_FOLDER = 'static'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload/video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video part"}), 400

    video = request.files['video']

    if video.filename == '':
        return jsonify({"error": "No selected video"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(filepath)
    return jsonify({"message": "Видео успешно загружено!"}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return 'No file part'
    file = request.files['image']
    if file.filename == '':
        return 'No selected file'
    file_path = f"static/{file.filename}"
    file.save(file_path)
    print(file_path)
    if os.path.exists(file_path):
        return 'File uploaded and saved successfully'
    else:
        return 'File not saved'
    return 'File uploaded successfully'

@app.route('/api/layout/<template_name>')
def get_layout(template_name):
    html = render_template(template_name + ".html")
    return jsonify(data=html)

@app.route('/api/tag/<tag_name>')
def get_tag(tag_name):

    template_folder_path = 'tags/'
    template_path = '{}/{}.html'.format(template_folder_path, tag_name)

    try:
        with open(template_path, 'r') as file:
            html = file.read()

    except FileNotFoundError:
        return 'HTML template not found', 404

    return jsonify(data=html)

@app.route('/static/&lt;path:path&gt;')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/api/main/<main_name>')
def get_main(main_name):

    template_folder_path = 'main/'
    template_path = '{}/{}.html'.format(template_folder_path, main_name)

    try:
        with open(template_path, 'r') as file:
            html = file.read()

    except FileNotFoundError:
        return 'HTML template not found', 404

    return jsonify(data=html)

@app.route('/api/main/js/<js_name>')
def get_main_js(js_name):
    js_folder_path = 'main/js'
    js_path = os.path.join(js_folder_path, js_name)

    try:
        with open(js_path, 'r') as file:
            js_content = file.read()

    except FileNotFoundError:
        return 'JS file not found', 404

    return jsonify(data=js_content)

@app.route('/api/main/css/<css_name>')
def get_main_css(css_name):
    css_folder_path = 'main/css'
    css_path = os.path.join(css_folder_path, css_name)

    try:
        with open(css_path, 'r') as file:
            css_content = file.read()

    except FileNotFoundError:
        return 'CSS file not found', 404

    return jsonify(data=css_content)

if __name__ == '__main__':
    app.run(debug=True)
