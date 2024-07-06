import os
from pathlib import Path
import time
import pytest
import subprocess
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join('..', 'python_client', 'client')))
from api_client import APIClient

PRESENTATION_PATH_1 = Path(os.path.abspath(os.path.join('sample_presentation', 'Chapter_4_V7.01.pptx')))
PRESENTATION_PATH_2 = Path(os.path.abspath(os.path.join('sample_presentation', 'Chapter_6_5-6.pptx')))
UPLOAD_DIR = Path(os.path.abspath(os.path.join('..', 'web_app', 'shared_uploads')))
OUTPUT_DIR = Path(os.path.abspath(os.path.join('..', 'web_app', 'shared_outputs')))

# SLEEP_TIME is long because the gpt_explainer takes a long time to process the file. can be reduced , depending on your system
SLEEP_TIME = 250

def delete_files():
    '''Deletes all files in the upload and output directories'''
    for folder in [UPLOAD_DIR, OUTPUT_DIR]:
        for file in folder.glob('*'):
            file.unlink()


@pytest.fixture(scope="module")
def setup_web_app():
    '''Starts the web app server'''
    web_app_script_path = os.path.abspath(os.path.join('..', 'web_app', 'app', 'main.py'))
    web_app_process = subprocess.Popen(['python3', web_app_script_path])
    time.sleep(5)
    yield
    web_app_process.terminate()

@pytest.fixture(scope="module")
def setup_gpt_explainer():
    '''Starts the gpt_explainer server'''
    gpt_explainer_script_path = os.path.abspath(os.path.join('..', 'gpt_explainer', 'scripts', 'main.py'))
    gpt_explainer_process = subprocess.Popen(['python3', gpt_explainer_script_path])
    yield
    gpt_explainer_process.terminate()

@pytest.fixture(scope="module")
def api_client():
    '''Returns an instance of the APIClient'''
    return APIClient()

def test_upload_method_returns_uid(api_client, setup_web_app, setup_gpt_explainer):
    '''
    Test that the upload method returns a uid
    The upload method should return a uid when a valid file is uploaded
    '''
    uid = api_client.upload(PRESENTATION_PATH_2)
    assert uid is not None and isinstance(uid, str) 
    delete_files()

def test_upload_creates_file(api_client, setup_web_app, setup_gpt_explainer):
    '''
    Test that the upload method creates a file
    The upload method should create a file in the shared_uploads folder
    '''
    uid = api_client.upload(PRESENTATION_PATH_2)
    upload_folder = Path(UPLOAD_DIR) 
    uploaded_files = list(upload_folder.glob(f'*_{uid}.pptx'))
    
    assert len(uploaded_files) == 1, f"No file or multiple files found with pattern '*_{uid}.pptx' in {upload_folder}"
    assert uploaded_files[0].exists(), f"The file {uploaded_files[0]} does not exist."
    delete_files()

def test_explainer_processes_new_files(api_client, setup_web_app, setup_gpt_explainer):
    '''
    Test that the explainer processes new files
    The explainer should process new files uploaded by the client
    '''
    uid_1 = api_client.upload(PRESENTATION_PATH_1)
    uid_2 = api_client.upload(PRESENTATION_PATH_2)
    time.sleep(SLEEP_TIME)
    status_1 = api_client.status(uid_1)
    status_2 = api_client.status(uid_2)
    assert status_1.is_done() and status_2.is_done()
    assert status_1.explanation is not None and status_2.explanation is not None
    delete_files()

def test_client_raises_errors_for_invalid_uid(api_client, setup_web_app, setup_gpt_explainer):
    '''
    Test that the client raises an error for an invalid uid
    '''
    with pytest.raises(Exception):
        api_client.status("invalid_uid")

def test_status_method_returns_pending(api_client, setup_web_app, setup_gpt_explainer):
    '''Test that the status method returns pending if we check the status immediately after uploading'''
    uid = api_client.upload(PRESENTATION_PATH_2)
    status = api_client.status(uid)
    assert status.status == 'pending'
    delete_files()

def test_full_cycle(api_client, setup_web_app, setup_gpt_explainer):
    '''Test the full cycle of uploading a file, waiting for the status to be updated and checking the status'''
    uid_1 = api_client.upload(PRESENTATION_PATH_1)
    uid_2 = api_client.upload(PRESENTATION_PATH_2)
    assert uid_1 is not None and uid_2 is not None
    assert api_client.status(uid_1).status == 'pending' and api_client.status(uid_2).status == 'pending'

    time.sleep(SLEEP_TIME)  
    status_1 = api_client.status(uid_1)
    status_2 = api_client.status(uid_2)

    assert status_1.is_done() and status_2.is_done()
    assert status_1.explanation is not None and status_2.explanation is not None
    
    assert len(list(UPLOAD_DIR.glob('*'))) == len(list(OUTPUT_DIR.glob('*')))
    delete_files()

if __name__ == "__main__":
    
    pytest.main(['-v', 'sys_test.py'])