from flask import Flask
from flask_ckeditor import CKEditor
import json
from flask_mail import Mail
import os


# Create a Flask Instance
app = Flask(__name__, template_folder='../templates', static_folder="../static")


# Configure Json
with open('config.json', 'r') as c:
    params = json.load(c) ["params"]


# Add CKEditor
ckeditor = CKEditor(app)
app.config['CKEDITOR_ENABLE_CODESNIPPET'] = True


# setting up and intialising flask mail
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password'])

mail = Mail(app)


# Profile pic upload directory
UPLOAD_FOLDER = 'static/imgs/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
