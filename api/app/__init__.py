from flask import Flask

UPLOAD_FOLDER = '../uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

app = Flask(__name__, static_folder="../../frontend/dist", static_url_path='/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import routes