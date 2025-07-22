from flask import Flask, request, jsonify, send_from_directory
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MongoDB Atlas connection
uri = "mongodb+srv://nandukumar9980:kumar456@cluster0.ecnna5x.mongodb.net/student-form?retryWrites=true&w=majority"
try:
    client = MongoClient(uri, serverSelectionTimeoutMS=30000)
    client.admin.command('ping')
    print("Connected to MongoDB Atlas")
except Exception as e:
    print(f"MongoDB connection error: {e}")
    exit(1)

db = client['student-form']
students_collection = db['students']

# File upload configuration
UPLOAD_FOLDER = './Uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/submit', methods=['POST'])
def submit_form():
    try:
        # Get form data
        form_data = {
            'full_name': request.form.get('full_name'),
            'father_name': request.form.get('father_name'),
            'mother_name': request.form.get('mother_name'),
            'gender': request.form.get('gender'),
            'phone_number': request.form.get('phone_number'),
            'father_mobile_no': request.form.get('father_mobile_no'),
            'mother_mobile_no': request.form.get('mother_mobile_no'),
            'email': request.form.get('email'),
            'address': request.form.get('address'),
            'dob': datetime.strptime(request.form.get('dob'), '%Y-%m-%d'),
            'nationality': request.form.get('nationality'),
            'reservation_category': request.form.get('reservation_category'),
            'reservation_category_other': request.form.get('reservation_category_other'),
            'matric_board': request.form.get('matric_board'),
            'matric_marks': request.form.get('matric_marks'),
            'intermediate': request.form.get('intermediate'),
            'intermediate_group': request.form.get('intermediate_group'),
            'intermediate_marks': request.form.get('intermediate_marks'),
            'degree': request.form.get('degree'),
            'course': request.form.get('course'),
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
                return jsonify({'error': f'Invalid {file_key} file type or no file selected'}), 400

        # Validate required fields
        required_fields = ['full_name', 'father_name', 'mother_name', 'gender', 'phone_number', 
                           'father_mobile_no', 'mother_mobile_no', 'email', 'address', 'dob', 
                           'nationality', 'reservation_category', 'matric_board', 'degree', 
                           'course', 'photo', 'signature']
        for field in required_fields:
            if not form_data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        # Save to MongoDB
        students_collection.insert_one(form_data)
        return jsonify({'message': 'Form submitted successfully'})

    except Exception as e:
        print(f"Error saving data: {e}")
        return jsonify({'error': f'Submission failed: {str(e)}'}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
