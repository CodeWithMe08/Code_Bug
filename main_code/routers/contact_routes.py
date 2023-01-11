from flask import render_template, request
from datetime import datetime 
import uuid as uuid
from initial import app, params, mail
from database import params, db
from models import Contacts

# Create a route decorator
#trim
#striptags

@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/', methods = ['GET','POST'])
# def index():
# 	if (request.method == 'POST'):
# 		name = request.form.get('name')
# 		email = request.form.get('email')
# 		phone = request.form.get('phone')
# 		message = request.form.get('message')

# 		entry = Contacts(name = name, email = email, phone_num = phone, msg = message, date = datetime.now())
# 		db.session.add(entry)
# 		db.session.commit()
# 		mail.send_message('New message from Blog by' + name,
# 						sender = email,
# 						recipients = [params['gmail-user']],
# 						body = message + "\n" + phone
# 						)
# 	return render_template("index.html", params = params)
