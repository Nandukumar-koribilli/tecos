from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)

# MongoDB Atlas connection
uri = "mongodb+srv://nandukumar9980:kumar456@cluster0.ecnna5x.mongodb.net/student-form?retryWrites=true&w=majority"
try:
    client = MongoClient(uri, serverSelectionTimeoutMS=30000)
    client.server_info()
    print("Connected to MongoDB Atlas")
except Exception as e:
    print(f"MongoDB connection error: {e}")
    exit(1)

db = client['student-form']
students_collection = db['students']

# File upload configuration
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_student_id(year, course):
    # Find the latest ID for the given year and course
    latest_doc = students_collection.find_one(
        {'year': year, 'course': course},
        sort=[('student_id', -1)]
    )
    if latest_doc and 'student_id' in latest_doc:
        # Extract the numeric part (last 5 digits) and increment
        last_id = latest_doc['student_id']
        numeric_part = int(last_id[-5:])
        new_numeric = numeric_part + 1
        new_id = f"{year}-{course}{new_numeric:05d}"
    else:
        # First ID for this year and course
        new_id = f"{year}-{course}25600"
    return new_id

@app.route('/api/submit', methods=['POST'])
def submit_form():
    try:
        # Get form data
        form_data = {
            'full_name': request.form.get('full_name'),
            'phone_number': request.form.get('phone_number'),
            'email': request.form.get('email'),
            'address': request.form.get('address'),
            'dob': datetime.strptime(request.form.get('dob'), '%Y-%m-%d'),
            'nationality': request.form.get('nationality'),
            'matric_board': request.form.get('matric_board'),
            'intermediate': request.form.get('intermediate'),
            'degree': request.form.get('degree'),
            'course': request.form.get('course'),
            'year': request.form.get('year'),
            'skills': request.form.get('skills'),
            'hobbies': request.form.get('hobbies'),
            'work_experience': request.form.get('work_experience')
        }

        # Handle file uploads
        for file_key in ['photo', 'signature']:
            if file_key not in request.files:
                return jsonify({'error': f'{file_key} is required'}), 400
            file = request.files[file_key]
            if file.filename == '':
                return jsonify({'error': f'No {file_key} selected'}), 400
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{file_key}_{int(datetime.now().timestamp())}{os.path.splitext(file.filename)[1]}")
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                form_data[file_key] = file_path
            else:
                return jsonify({'error': f'Invalid {file_key} file type'}), 400

        # Validate required fields
        required_fields = ['full_name', 'phone_number', 'email', 'address', 'dob', 'nationality', 
                           'photo', 'signature', 'matric_board', 'degree', 'course', 'year']
        for field in required_fields:
            if not form_data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        # Generate student ID
        current_year = datetime.now().year
        course_number = form_data['course']  # e.g., '01' for BSc Computer Science
        student_id = generate_student_id(str(current_year), course_number)
        form_data['student_id'] = student_id

        # Save to MongoDB
        students_collection.insert_one(form_data)
        return jsonify({'message': 'Form submitted successfully', 'student_id': student_id})

    except Exception as e:
        print(f"Error saving data: {e}")
        return jsonify({'error': 'Submission failed'}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(port=3000, debug=True)