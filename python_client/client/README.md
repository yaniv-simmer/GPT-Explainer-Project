# README

## Project: API Client for File Upload and Status Tracking

### Overview

This project provides a simple Python client for interacting with a web API that supports file uploads and status tracking. The client includes methods to upload files to a server and retrieve the status of these uploads.

### Features

- **File Upload**: Uploads a file to the server and returns a unique identifier (UID) if successful.
- **Status Check**: Retrieves the status of an uploaded file using its UID.

### Requirements

- Python 3.7+
- `requests` library

### Installation

1. **Clone the repository**:
   ```bas
   git clone https://github.com/your-repository/api-client.git
   cd api-client
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bas
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required packages**:
   ```bas
   pip install -r requirements.txt
   ```

### Usage

The client is implemented in the `APIClient` class, which provides methods to upload files and check the status of an upload.

#### Example

```python
from api_client import APIClient

# Initialize the client
client = APIClient(base_url="http://your-server-url")

# Upload a file
file_path = "path/to/your/file.txt"
uid = client.upload(file_path)
if uid:
    print(f"File uploaded successfully. UID: {uid}")

# Check the status of the uploaded file
if uid:
    status = client.status(uid)
    if status:
        print(f"Status: {status.status}")
        print(f"Filename: {status.filename}")
        print(f"Timestamp: {status.timestamp}")
        print(f"Explanation: {status.explanation}")
        if status.is_done():
            print("The file processing is complete.")
```

### File Structure

- **api_client.py**: Contains the `APIClient` class and the `Status` dataclass.
- **requirements.txt**: Lists the required packages for the project.

### Logging

The client uses Python's built-in logging module to provide informative messages about the operations performed, especially in cases of errors.

### Exception Handling

The client raises HTTP errors when requests fail. Ensure proper exception handling in your application to manage these errors.

### Methods

#### `APIClient.upload(file_path: str) -> Optional[str]`
Uploads a file to the server. Returns the UID of the uploaded file if successful, otherwise logs an error and raises an HTTP error.

- **Parameters**:
  - `file_path`: The path to the file to be uploaded.

- **Returns**:
  - The UID of the uploaded file if successful.

#### `APIClient.status(uid: str) -> Optional[Status]`
Fetches the status of an upload by its UID. Returns a `Status` object if successful, otherwise logs an error and raises an HTTP error.

- **Parameters**:
  - `uid`: The UID of the uploaded file.

- **Returns**:
  - A `Status` object containing the status information.

### Status Class

The `Status` class is a dataclass that represents the status of an uploaded file.

- **Attributes**:
  - `status`: The status of the file (e.g., 'done', 'processing').
  - `filename`: The name of the uploaded file.
  - `timestamp`: The timestamp of the status in `datetime` format.
  - `explanation`: An optional explanation of the status.

- **Methods**:
  - `from_json(data: dict) -> Status`: Creates a `Status` object from a JSON dictionary.
  - `is_done() -> bool`: Checks if the status is 'done'.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

### Contact

For any questions or issues, please contact [your-email@example.com](mailto:your-email@example.com).

---

Feel free to customize this README file further based on your specific project needs and details.
