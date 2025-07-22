from flask import Flask, render_template, request, redirect, url_for, jsonify, json
from werkzeug.utils import secure_filename
import os
from PrivateCAN.backend.parser import DBCParser
from PrivateCAN.backend.serializer import CANModelSerializer
from PrivateCAN.backend.models import *
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'dbc'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        parser = DBCParser()
        can_model = parser.parse_dbc_to_model(filepath)

        json_data = CANModelSerializer.to_json(can_model)

        return render_template('network.html',
                               network_data=json_data,
                               messages=can_model.messages,
                               signals=can_model.signals)

    return redirect(request.url)


@app.route('/api/parse', methods=['POST'])
def api_parse():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        parser = DBCParser()
        can_model = parser.parse_dbc_to_model(filepath)
        json_data = CANModelSerializer.to_json(can_model)

        return jsonify({
            "status": "success",
            "data": json.loads(json_data)
        })

    return jsonify({"error": "Invalid file type"}), 400


if __name__ == '__main__':
    app.run(debug=True)
