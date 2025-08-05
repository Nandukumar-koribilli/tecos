from pymongo import MongoClient
import pandas as pd

# MongoDB Atlas connection
uri = "mongodb+srv://nandukumar9980:kumar456@cluster0.ecnna5x.mongodb.net/student-form?retryWrites=true&w=majority"
client = MongoClient(uri, serverSelectionTimeoutMS=30000)
db = client['student-form']
students_collection = db['students']

# Fetch data
data = list(students_collection.find())

# Convert to DataFrame
df = pd.DataFrame(data)

# Select specific columns for display
columns_to_show = ['full_name', 'father_name', 'mother_name', 'gender', 'phone_number', 'email', 'course', 'submission_date']
df = df[columns_to_show]

# Format submission_date
df['submission_date'] = pd.to_datetime(df['submission_date']).dt.strftime('%Y-%m-%d %H:%M:%S')

# Save to Excel
df.to_excel('students_data.xlsx', index=False)
print("Data exported to 'students_data.xlsx'")
