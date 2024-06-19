import os
import pytest
import subprocess
import sys

input_presentation = os.path.abspath(os.path.join('..\presentations', 'Chapter_6_5-6.pptx'))
# print the working dir

output_file = os.path.abspath(os.path.join(os.getcwd(),'output', 'Chapter_6_5-6.json'))


def teardown_module():
    #output_file_ = os.path.abspath(os.path.join('..\output', 'Chapter_6_5-6.json'))
    if os.path.exists(output_file):
        os.remove(output_file)


def test_system():
    # Clean up the output file before the test
    if os.path.exists(output_file):
        os.remove(output_file)

    # Run the main script
    script_path = os.path.abspath(os.path.join('..\scripts', 'main.py'))
    print('\nfffff\n'+script_path)
    result = subprocess.run(['python3.10.exe',script_path, "--pptx_file_path", input_presentation], timeout=100)

    # Check the script executed without errors
    assert result.returncode == 0, "Script did not execute successfully"

    # print ls
    #print('\nllllllist\n'+os.listdir(os.path.abspath(os.path.join('..\output'))))
    print()
    print('\nrrrrr+ \n'+output_file)
    assert os.path.exists(output_file), "Output file was not created"

    

# def test_system():
#     '''
#     Test the system as a whole
#     '''
#     input_presentation = INPUT_PRESENTATION
#     output_file = EXPECTED_OUTPUT_FILE
#     print(f"Input file: {input_presentation}")
#     print(f"Expected output file: {output_file}")
#
#     w = subprocess.run(["python3.10.exe", r"..\scripts\main.py", "--pptx_file_path", input_presentation],
#                        capture_output=True)
#     print(f"Subprocess output: {w.stdout.decode()}")
#
#     assert os.path.exists(output_file), "Output file was not created"
#
#     if os.path.exists(output_file):
#         os.remove(output_file)
