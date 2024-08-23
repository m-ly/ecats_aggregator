from app import app
import os
from flask import request, jsonify, send_file
from werkzeug.utils import secure_filename
from .ready_report import create_ready_report
from .status_report import create_status_report
import time
import tempfile

DIRECTORY = 'uploads'

def wait_for_files(directory, expected_count):
    start_time = time.time()
    while len(os.listdir(directory)) < expected_count:
        if time.time() - start_time > 10:  
            raise Exception("Timeout waiting for files to be ready")
        time.sleep(0.5)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    try:
        script = request.form.get('script')
        with tempfile.TemporaryDirectory() as tempdir:
        
          if request.files:
            for key in request.files:
                file = request.files[key]
                filename = secure_filename(file.filename)
                file.save(os.path.join(DIRECTORY, filename))

            wait_for_files(DIRECTORY, len(request.files))
            
            
            if script == 'ready':
              create_ready_report(DIRECTORY)
              report_filename = 'monthly_ready_report.xlsx'   
              download_url = f'/download/{report_filename}'
            else:
              create_status_report(DIRECTORY)
              report_filename = 'monthly_status_report.xlsx' 
              download_url = f'/download/{report_filename}'
          
            
            return jsonify({"status": 1, "download_url": download_url }) 
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({"status": 0})
    

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    uploads_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))
    print(uploads_path)
    try:
      file_path = os.path.join(uploads_path, filename)
      response = send_file(file_path, as_attachment=True, mimetype= 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception as e:
      print(f'Error: {e}')
      response = jsonify({"status": 0})

    for root, dirs, files in os.walk(uploads_path):
       for file in files:
         file_to_remove = os.path.join(root, file)
         os.remove(file_to_remove)

    return response