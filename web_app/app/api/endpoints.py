from flask import Blueprint, request, jsonify
import os
import uuid
from datetime import datetime
import glob

api_bp = Blueprint('api', __name__)
UPLOAD_FOLDER = 'web_app/uploads/'
PROCESSED_FOLDER = 'web_app/outputs/'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)



@api_bp.route('/upload', methods=['POST'])
def upload_file():
    '''
    Uploads a file to the server and returns a unique identifier (UID) for the file
    
    Returns:
        - JSON response with the UID of the uploaded file
    '''
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Ensure UID is unique for each file
    uid = uuid.uuid4().hex    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = os.path.join(UPLOAD_FOLDER, f"{file.filename}_{timestamp}_{uid}")
    
    file.save(filename)
        
    return jsonify({'uid': uid}), 200



@api_bp.route('/status/<uid>', methods=['GET'])
def check_status(uid):
    '''
    Checks the status of a file upload job. If the job is done, the explanation is also returned

    Parameters:
        - uid (str): The unique identifier of the file upload job
        
    Returns:
        - JSON response with the status of the job
    '''
    original_file_found = False
    original_filename = ""
    timestamp = ""
    explanation = None
    
    files = glob.glob(os.path.join(UPLOAD_FOLDER, f"*_{uid}"))
    
    if files:
        file_path = files[0]
        original_file_found = True
        parts = os.path.basename(file_path).rsplit('_', 2)
        original_filename, timestamp = parts[0], parts[1]
    else:
        original_file_found = False
    
    if not original_file_found:
        return jsonify({'status': 'not found'}), 404
    
    result_file = os.path.join(PROCESSED_FOLDER, f"{uid}_result.json")
    if os.path.exists(result_file):
        with open(result_file, 'r') as f:
            explanation = f.read()
        status = 'done'
    else:
        status = 'pending'
    
    return jsonify({
        'status': status,
        'filename': original_filename if original_file_found else "",
        'timestamp': timestamp if original_file_found else "",
        'explanation': explanation if original_file_found else None
    }), 200

