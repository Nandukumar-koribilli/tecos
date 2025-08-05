Student Application Form Project
Overview
This project is a web-based student application form for Gayatri Vidya Parishad College for Degree and PG Courses (Autonomous). It includes a frontend interface, a Flask backend, and MongoDB for data storage.
Features

Interactive form for personal, educational, and additional details.
File upload for photos and signatures.
Data storage in MongoDB Atlas.
Data export to Excel.
Responsive and modern design.

Technologies Used

Frontend: HTML, CSS
Backend: Python, Flask
Database: MongoDB Atlas
Libraries: pymongo, pandas, openpyxl, flask-cors, werkzeug

Setup Instructions
Prerequisites

Python 3.x
MongoDB Atlas account
pip (Python package manager)

Installation

Clone the repository:git clone <repository-url>
cd <repository-folder>


Create a virtual environment and activate it:python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install required packages:pip install flask pymongo pandas openpyxl flask-cors werkzeug


Set up MongoDB Atlas:
Create a cluster and get the connection URI.
Update the uri in app.py and export_to_excel.py with your MongoDB Atlas URI.


Run the Flask app:python app.py


Open index.html in a browser or use a local server.

Usage

Fill and submit the form to save data to MongoDB.
Use export_to_excel.py to export data to students_data.xlsx.
Open the .xlsx file in Excel to view data in tabular form.

API Endpoints

POST /api/submit: Submit a new student application.
GET /api/students: Retrieve all student records.
GET /uploads/<filename>: Access uploaded files.

Contributing
Contributions are welcome. Fork the repository and submit a pull request.
License
MIT License
