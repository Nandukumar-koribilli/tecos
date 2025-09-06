from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from flask_cors import CORS
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

app = Flask(__name__)
CORS(app)

# --- MongoDB Configuration ---
# Your connection string
MONGO_URI = "mongodb+srv://nandukumar9980:kumar456@cluster0.ecnna5x.mongodb.net/student-form?retryWrites=true&w=majority"
try:
    # Establish a connection to the MongoDB server
    client = MongoClient(MONGO_URI)
    # Test the connection
    client.admin.command('ping')
    print("MongoDB connection successful.")
    # Select the database and collection
    db = client['student-form']
    collection = db['students']
except ConnectionFailure as e:
    print(f"Could not connect to MongoDB: {e}")
    client = None
except Exception as e:
    print(f"An error occurred during MongoDB setup: {e}")
    client = None

# Configuration for file uploads and the output Excel file
UPLOAD_FOLDER = './Uploads'
EXCEL_FILE = 'students_data.xlsx'
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
            'phone_number': request.form.get('phone_country_code', '') + request.form.get('phone_number', ''),
            'father_phone_number': request.form.get('father_phone_country_code', '') + request.form.get('father_phone_number', ''),
            'mother_phone_number': request.form.get('mother_phone_country_code', '') + request.form.get('mother_phone_number', ''),
            'email': request.form.get('email'),
            'permanent_address': request.form.get('permanent_address'),
            'address': request.form.get('address'),
            'dob': request.form.get('dob'),
            'nationality': request.form.get('nationality'),
            'other_nationality': request.form.get('other_nationality'),
            'reservation_category': request.form.get('reservation_category'),
            'other_reservation_category': request.form.get('other_reservation_category'),
            'matric_board': request.form.get('matric_board'),
            'matric_marks': request.form.get('matric_marks'),
            'intermediate_college': request.form.get('intermediate_college'),
            'intermediate_group': request.form.get('intermediate_group'),
            'intermediate_marks': request.form.get('intermediate_marks'),
            'degree': request.form.get('degree'),
            'course': request.form.get('course'),
            'skills': request.form.get('skills'),
            'hobbies': request.form.get('hobbies'),
            'work_experience': request.form.get('work_experience'),
            'submission_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Handle file uploads
        for file_key in ['photo', 'signature']:
            if file_key in request.files:
                file = request.files[file_key]
                if file and allowed_file(file.filename):
                    filename = secure_filename(f"{file_key}_{int(datetime.now().timestamp())}{os.path.splitext(file.filename)[1]}")
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    form_data[file_key] = file_path
        
        # --- Save to MongoDB ---
        if client:
            # Using .copy() is a good practice to avoid any potential side-effects
            collection.insert_one(form_data.copy())
            print("Data saved to MongoDB.")
        else:
            print("MongoDB client not available. Skipping database save.")

        # Save to Excel
        new_df = pd.DataFrame([form_data])
        try:
            with pd.ExcelWriter(EXCEL_FILE, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                startrow = writer.book.worksheets[0].max_row
                new_df.to_excel(writer, index=False, header=False, startrow=startrow, sheet_name='Sheet1')
        except FileNotFoundError:
            new_df.to_excel(EXCEL_FILE, index=False)
        
        return jsonify({'message': 'Form submitted successfully'})

    except Exception as e:
        print(f"Error saving data: {e}")
        return jsonify({'error': f'Submission failed: {str(e)}'}), 500

@app.route('/api/students', methods=['GET'])
def get_students():
    try:
        # This route still reads from the Excel file.
        # If you want it to read from MongoDB, you'd change it here.
        df = pd.read_excel(EXCEL_FILE)
        df = df.fillna('')
        records = df.to_dict(orient='records')
        return jsonify(records)
    except FileNotFoundError:
        return jsonify([])
    except Exception as e:
        print(f"Error retrieving data: {e}")
        return jsonify({'error': f'Retrieval failed: {str(e)}'}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(port=3000, debug=True, use_reloader=False)