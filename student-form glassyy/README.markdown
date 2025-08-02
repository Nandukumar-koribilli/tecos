# Student Application Form Project

## Overview
This project is a web-based student application form for Gayatri Vidya Parishad College for Degree and PG Courses (Autonomous). It includes a frontend interface and a backend API to handle form submissions and store data in MongoDB.

## Features
- User-friendly form with personal, educational, and additional details.
- File upload support for photos and signatures.
- Data storage in MongoDB Atlas.
- Responsive design with modern styling.

## Technologies Used
- **Frontend**: HTML, CSS
- **Backend**: Python, Flask
- **Database**: MongoDB Atlas
- **Other**: CORS for cross-origin requests

## Setup Instructions

### Prerequisites
- Python 3.x
- MongoDB Atlas account
- pip (Python package manager)

### Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Install required Python packages:
   ```
   pip install flask pymongo flask-cors werkzeug
   ```
3. Set up MongoDB Atlas:
   - Create a cluster and get the connection URI.
   - Replace the `uri` in `app.py` with your MongoDB Atlas URI.
4. Run the application:
   ```
   python app.py
   ```
5. Open `index.html` in a web browser or use a local server.

## Usage
- Fill out the form with the required details.
- Upload a photo and signature.
- Submit the form to save data to the database.
- View submissions via the `/api/students` endpoint.

## API Endpoints
- `POST /api/submit`: Submit a new student application.
- `GET /api/students`: Retrieve all student records.
- `GET /uploads/<filename>`: Access uploaded files.

## Contributing
Contributions are welcome. Please fork the repository and submit a pull request.

## License
MIT License