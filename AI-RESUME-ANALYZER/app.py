from flask import Flask, render_template, request
import os
import PyPDF2
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to extract text from PDF
def extract_text(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text().lower()
    except Exception as e:
        print("Error reading PDF:", e)
    return text

# Function to calculate matching score
def calculate_score(resume_text, job_desc):
    jd_words = job_desc.lower().split()
    
    if len(jd_words) == 0:
        return 0
    
    match_count = sum(1 for word in jd_words if word in resume_text)
    score = (match_count / len(jd_words)) * 100
    
    return round(score, 2)

# Main route
@app.route('/', methods=['GET', 'POST'])
def index():
    score = None

    if request.method == 'POST':
        if 'resume' not in request.files:
            return "No file part"

        file = request.files['resume']
        job_desc = request.form.get('jobdesc', '')

        if file.filename == '':
            return "No file selected"

        if file:
            # Secure filename
            filename = secure_filename(file.filename)

            # Save file
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Extract text
            resume_text = extract_text(filepath)

            # Calculate score
            score = calculate_score(resume_text, job_desc)

    return render_template('index.html', score=score)

# Run app
if __name__ == '__main__':
    app.run(debug=True)