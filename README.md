
# PPTX files GPT Explainer

## Overview

This project is designed to explain PowerPoint presentations using the GPT-3.5 AI model. It includes multiple components such as a Python client, a web application, and various scripts to facilitate the processing and explanation of presentation files.

## Project Structure

- **gpt_explainer**: Contains the core scripts and outputs for processing and explaining presentations.
  - `scripts`: Python scripts for asynchronous requests, GPT integration, and PowerPoint text extraction.
  - `outputs`: JSON files with the output explanations.
  - `presentations`: Sample PowerPoint files used in the project.
  - `tests`: Test scripts for system testing.
- **python_client**: Python client for interacting with the GPT Explainer API.
  - `client`: Contains the API client implementation.
  - `README.md`: Documentation for the Python client.
  - `pyproject.toml`: Configuration file for the Python client.
- **web_app**: Web application for interacting with the GPT Explainer service.
  - `app`: Core application code including configuration and API endpoints.
  - `logs`: Logs for API and GPT explainer activities.
- **test**: Contains sample presentations for testing.

## Installation

### Prerequisites

- Python 3.10+
- Pip

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Scaleup-Excellenteam/final-exercise-yaniv-simmer/tree/Development-part-2
   cd final-exercise-yaniv-simmer-Development-part-2
Install dependencies:
```bash
pip install -r requirements.txt
```
## Usage
### GPT explainer
To run the main script for explaining a presentation:

```bash
python gpt_explainer/scripts/main.py 
```
This runs continuesly and checks if any new files where uploded and need to be explained.
### Web Application
To start the web application:

```bash
cd web_app/app
python main.py
```
Access the web app at http://localhost:5000.

### Python Client
To use the Python client, import and initialize the API client:

```bash
cd python_client
pip install .
```
please note the python_client's package README
## Design
The project is designed with modularity in mind, separating core functionalities into distinct components:

### GPT Integration:
Handles the interaction with the GPT-3.5 model.
### Async Requests:
Manages asynchronous HTTP requests to the GPT API.
### Text Extraction: 
Extracts text from PowerPoint presentations for processing.
### Web API: 
Provides endpoints for interacting with the explainer service.
