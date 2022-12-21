from flask import Flask
from flask_login import LoginManager
import uuid as uuid
from ititialize import app
from database import params, db
from models import Users, Posts, Contacts
import post_routes
import auth
import user_routes
import administrator
import contact_routes
import custom_error


if __name__=="__main__":
    app.run(debug=True)