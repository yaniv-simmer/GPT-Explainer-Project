import os
import pytest
import subprocess
import sys

INPUT_FILE = os.path.abspath(os.path.join('..\presentations', 'Chapter_6_5-6.pptx'))
OUTPUT_FILE = os.path.abspath(os.path.join(os.getcwd(),'output', 'Chapter_6_5-6.json'))


def teardown_module():
    """
    This function is called after the module is done executing.
    It checks if the output file exists and removes it if it does.
    """
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)


def test_system():
    """
    This function tests the system by running the main script with the input presentation file.
    It first checks if the output file exists and removes it if it does.
    Then it runs the main script with the input presentation file as an argument.
    It asserts that the script executed successfully by checking the return code.
    Finally, it asserts that the output file was created.
    """
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    script_path = os.path.abspath(os.path.join('..\scripts', 'main.py'))
    result = subprocess.run(['python3',script_path, "--pptx_file_path", INPUT_FILE], timeout=250)

    assert result.returncode == 0, "Script did not execute successfully"

    assert os.path.exists(OUTPUT_FILE), "Output file was not created"
    teardown_module()


