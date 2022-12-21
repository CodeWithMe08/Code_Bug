from flask import flash, render_template, redirect, url_for
from flask_login import login_user, login_required,LoginManager, logout_user
from werkzeug.security import generate_password_hash, check_password_hash 
import uuid as uuid
from web_forms import UserForm,LoginForm
from initial import app, params
from database import params, db
from models import Users 


# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

# Registration
@app.route('/register/add', methods=['GET', 'POST'])
def register():
	name = None
	form = UserForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None:
			# Hash the password!!!
			hashed_pw = generate_password_hash(form.password_hash.data, 'sha256')
			user = Users(username=form.username.data, name=form.name.data, email=form.email.data, password_hash=hashed_pw)
			db.session.add(user)
			db.session.commit()
		name = form.name.data
		form.name.data = ''
		form.username.data = ''
		form.email.data = ''
		form.password_hash.data = ''
		flash("Registration Completed!")
	our_users = Users.query.order_by(Users.date_added)
	return render_template("register.html", form=form,name=name,our_users=our_users,params=params)


# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(username=form.username.data).first()
		if user:
			# Check the hash
			if check_password_hash(user.password_hash, form.password.data):
				login_user(user)
				return redirect(url_for('index'))
			else:
				flash("Wrong Password - Try Again!")
		else:
			flash("Wrong username or password! Try again...")
	return render_template('login.html', form=form)


# Logout Page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	flash("You Have Been Logged Out!  Thanks For Stopping By...")
	return redirect(url_for('login'))
