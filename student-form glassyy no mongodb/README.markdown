# Student Application Form Project

## Overview
Flask backend (app.py) handles student form submissions, saves data to `students_data.xlsx`, and provides API to view data. Frontend (index.html) is an HTML form for submissions.

## Setup
1. Install dependencies: `pip install flask flask-cors pandas openpyxl werkzeug`
2. Create `Uploads` folder.
3. Run: `python app.py`

## Endpoints
- POST `/api/submit`: Submit form data and files.
- GET `/api/students`: Retrieve all student data.

## Usage
Open `index.html` in browser to submit form. View data via `/api/students`.