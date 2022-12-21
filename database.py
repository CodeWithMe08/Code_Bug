from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid as uuid
import json
from ititialize import app, params

# SQLite DB
#app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
# MySQL DB
#app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
# postgres DB
app.config['SQLALCHEMY_DATABASE_URI'] = params['postgres_uri']

#'HEROKU_POSTGRESQL_COPPER_URL: params['postgres_copper_uri']

app.config['SECRET_KEY'] = params['secret_key']

# Initialize The Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
