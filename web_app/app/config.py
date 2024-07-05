import os
from pathlib import Path

current_dir = Path(__file__).parent.parent

# in case other scripts need to access these directories in the future
os.environ['OUTPUTS_DIR'] = str(current_dir / 'shared_outputs')
os.environ['UPLOADS_DIR'] = str(current_dir / 'shared_uploads')

outputs_dir = os.getenv('OUTPUTS_DIR')
uploads_dir = os.getenv('UPLOADS_DIR')

os.makedirs(outputs_dir, exist_ok=True)
os.makedirs(uploads_dir, exist_ok=True)

OUTPUTS_FOLDER = Path(outputs_dir)
UPLOADS_FOLDER = Path(uploads_dir)


