from flask import Blueprint, request, jsonify
from pathlib import Path
import uuid
from datetime import datetime
import logging
import sys
import os
from typing import Tuple, Optional
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import OUTPUTS_FOLDER, UPLOADS_FOLDER

FILE_NOT_FOUND_MSG = 'file not found'

LOG_FILE = Path(__file__).parent.parent.parent.resolve() / 'logs' /'api_logs'/ 'api_logs.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

api_bp = Blueprint('api', __name__)

class FileManager:
    @staticmethod
    def save_file(file, folder: Path, filename: str) -> None:
        """Saves a file to the specified folder."""
        try:
            folder.mkdir(parents=True, exist_ok=True)
            file_path = folder / filename
            file.save(file_path)
        except Exception as e:
            logging.error(f"Error saving file: {e}")
            raise

    @staticmethod
    def find_file(folder: Path, pattern: str) -> Optional[Path]:
        """Finds a file by pattern."""
        files = list(folder.glob(pattern))
        return files[0] if files else None

    @staticmethod
    def read_file(file_path: Path) -> str:
        """Reads content from a file."""
        try:
            with file_path.open('r') as file:
                return file.read()
        except Exception as e:
            logging.error(f"Error reading file: {e}")
            raise

@api_bp.route('/upload', methods=['POST'])
def upload_file() -> Tuple[jsonify, int]:
    """Uploads a file to the server and returns a unique identifier (UID) for the file."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    uid = uuid.uuid4().hex    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{file.filename[:-5]}_{timestamp}_{uid}.pptx"
    
    FileManager.save_file(file, UPLOADS_FOLDER, filename)
        
    return jsonify({'uid': uid}), 200

@api_bp.route('/status/<uid>', methods=['GET'])
def check_status(uid: str) -> Tuple[jsonify, int]:
    """Checks the status of a file upload job."""
    pattern = f"*_{uid}.pptx"
    file_path = FileManager.find_file(UPLOADS_FOLDER, pattern)
    
    if not file_path:
        return jsonify({'status': FILE_NOT_FOUND_MSG}), 404
    
    parts = file_path.name.rsplit('_', 2)
    original_filename, timestamp = parts[0], parts[1]
    
    result_file = OUTPUTS_FOLDER / f"{original_filename}_{timestamp}_{uid}.json"
    if result_file.exists():
        explanation = FileManager.read_file(result_file)
        status = 'done'
    else:
        status = 'pending'
    
    return jsonify({
        'status': status,
        'filename': original_filename,
        'timestamp': timestamp,
        'explanation': explanation if status == 'done' else None
    }), 200



@api_bp.route('/shared_dir', methods=['GET'])
def get_shared_dirs() -> Tuple[jsonify, int]:    
    """ Returns the shared directories for uploads and outputs """
    return jsonify({
        'uploads_dir': str(UPLOADS_FOLDER),
        'outputs_dir': str(OUTPUTS_FOLDER)
    }), 200