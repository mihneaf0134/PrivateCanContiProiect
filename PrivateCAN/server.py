from flask import Flask, render_template, request, redirect, url_for, jsonify, json, session
from werkzeug.utils import secure_filename
import os
from PrivateCAN.backend.parser import DBCParser
from PrivateCAN.backend.serializer import CANModelSerializer
from PrivateCAN.backend.models import *

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'dbc'}
app.secret_key = 'your_secret_key_here'  # Needed for session

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/connect', methods=['POST'])
def connect():
    # Here you would implement actual CAN connection logic
    return jsonify({'status': 'connected'})


@app.route('/upload')
def upload_page():
    return render_template('upload.html')


@app.route('/upload_dbc', methods=['POST'])
def upload_dbc():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "Empty filename"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            parser = DBCParser()
            can_model = parser.parse_dbc_to_model(filepath)

            # Use your serializer to properly convert to dict
            network_data = CANModelSerializer.to_dict(can_model)

            # Store serializable data in session
            session['network_data'] = network_data
            session['messages'] = network_data['messages']
            session['signals'] = network_data['signals']
            session['filename'] = filename

            return jsonify({
                "success": True,
                "filename": filename,
                "message_count": len(network_data['messages']),
                "signal_count": len(network_data['signals'])
            })
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    return jsonify({"success": False, "error": "Invalid file type"}), 400


@app.route('/network')
def network_page():
    network_data = session.get('network_data', None)
    messages = session.get('messages', [])
    signals = session.get('signals', [])
    filename = session.get('filename', 'No file loaded')
    return render_template('network.html',
                           network_data=network_data,
                           messages=messages,
                           signals=signals,
                           filename=filename)


@app.route('/signals')
def signals_page():
    messages = session.get('messages', [])
    signals = session.get('signals', [])
    filename = session.get('filename', 'No file loaded')
    return render_template('signals.html',
                           messages=messages,
                           signals=signals,
                           filename=filename)


@app.route('/optimize')
def optimize_page():
    return render_template('optimize.html')

@app.route('/save')
def save_page():
    network_data = session.get('network_data', None)
    return render_template('save.html', network_data=network_data)

@app.route('/api/update_signal', methods=['POST'])
def update_signal():
    data = request.get_json()
    # Here you would implement actual signal update logic
    print("Signal updated:", data)
    return jsonify({"status": "success"})

@app.route('/api/update_message', methods=['POST'])
def update_message():
    data = request.get_json()
    # Here you would implement actual message update logic
    print("Message updated:", data)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)