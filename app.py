from flask import Flask, flash, render_template,flash,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from werkzeug.security import generate_password_hash, check_password_hash 
from werkzeug.utils import secure_filename
from datetime import datetime 
import uuid as uuid
from web_forms import UserForm,PostForm,LoginForm,PasswordForm,SearchForm
import json
import os
import math
from sqlalchemy.sql import func

# Configure Json
with open('config.json', 'r') as c:
    params = json.load(c) ["params"]

# Create a Flask Instance
app = Flask(__name__)

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

# Profile pic upload directory
UPLOAD_FOLDER = 'static/imgs/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

# Create a route decorator
#trim
#striptags
@app.route('/', methods = ['GET','POST'])
def index():
	if (request.method == 'POST'):
		name = request.form.get('name')
		email = request.form.get('email')
		phone = request.form.get('phone')
		message = request.form.get('message')

		entry = Contacts(name = name, email = email, phone_num = phone, msg = message, date = datetime.now())
		db.session.add(entry)
		db.session.commit()
		mail.send_message('New message from Blog by' + name,
						sender = email,
						recipients = [params['gmail-user']],
						body = message + "\n" + phone
						)
	return render_template("index.html", params = params)


@app.route('/python')
@login_required
def python():
	# Filter all the posts from the database
	posts = Posts.query.filter_by(category = 'python').all()

	last = math.ceil(len(posts)/int(params['no_of_posts']))
	page = request.args.get('page')
	if (not str(page).isnumeric()):
		page = 1
	page = int(page)
	posts = posts[(page-1)*int(params['no_of_posts']):(page-1)*int(params['no_of_posts'])+ int(params['no_of_posts'])]
	if page == 1:
		prev = "#"
		next = "/python?page="+ str(page+1)
	elif page == last:
		prev = "/python?page="+ str(page-1)
		next = "#"
	else:
		prev = "/python?page="+ str(page-1)
		next = "/python?page="+ str(page+1)
	return render_template('posts.html', params=params, posts=posts, prev=prev, next=next)


@app.route('/database')
@login_required
def database():
	# Filter all the posts from the database
	posts = Posts.query.filter_by(category = 'database')
	return render_template("posts.html", posts=posts)


@app.route('/automation')
@login_required
def automation():
	# Filter all the posts from the database
	posts = Posts.query.filter_by(category = 'automation')
	return render_template("posts.html", posts=posts)


@app.route('/html')
@login_required
def html():
	# Filter all the posts from the database
	posts = Posts.query.filter_by(category = 'html')
	return render_template("posts.html", posts=posts)


@app.route('/web_framework')
@login_required
def web_framework():
	# Filter all the posts from the database
	posts = Posts.query.filter_by(category = 'web_framework')
	return render_template("posts.html", posts=posts)


@app.route('/git')
@login_required
def git():
	# Filter all the posts from the database
	posts = Posts.query.filter_by(category = 'git')
	return render_template("posts.html", posts=posts)


@app.route('/basic')
@login_required
def basic():
	# Filter all the posts from the database
	posts = Posts.query.filter_by(category = 'basic')
	return render_template("posts.html", posts=posts)


@app.route('/code')
@login_required
def code():
	# Filter all the posts from the database
	posts = Posts.query.filter_by(category = 'code').all()

	last = math.ceil(len(posts)/int(params['no_of_posts']))
	page = request.args.get('page')
	if (not str(page).isnumeric()):
		page = 1
	page = int(page)
	posts = posts[(page-1)*int(params['no_of_posts']):(page-1)*int(params['no_of_posts'])+ int(params['no_of_posts'])]
	if page == 1:
		prev = "#"
		next = "/code?page="+ str(page+1)
	elif page == last:
		prev = "/code?page="+ str(page-1)
		next = "#"
	else:
		prev = "/code?page="+ str(page-1)
		next = "/code?page="+ str(page+1)
	return render_template('posts.html', params=params, posts=posts, prev=prev, next=next)


@app.route('/project')
@login_required
def project():
	# Filter all the posts from the database
	posts = Posts.query.filter_by(category = 'project')
	return render_template("posts.html", posts=posts)


@app.route('/posts')
@login_required
def posts():
	# Grab all the posts from the database
	posts = Posts.query.order_by(func.random())
	postss = Posts.query.filter_by().all()

	last = math.ceil(len(postss)/int(params['no_of_posts']))
	page = request.args.get('page')
	if (not str(page).isnumeric()):
		page = 1
	page = int(page)
	posts = posts[(page-1)*int(params['no_of_posts']):(page-1)*int(params['no_of_posts'])+ int(params['no_of_posts'])]
	if page == 1:
		prev = "#"
		next = "/posts?page="+ str(page+1)
	elif page == last:
		prev = "/posts?page="+ str(page-1)
		next = "#"
	else:
		prev = "/posts?page="+ str(page-1)
		next = "/posts?page="+ str(page+1)
	return render_template('posts.html', params=params, posts=posts, prev=prev, next=next)


# Create post endpoint
@app.route('/posts/<int:id>')
@login_required
def post(id):
	post = Posts.query.get_or_404(id)
	return render_template('post.html', post=post)


# Pass Stuff To Navbar
@app.context_processor
def base():
	form = SearchForm()
	return dict(form=form)


# Create Search Function
@app.route('/search', methods=["POST"])
@login_required
def search():
	form = SearchForm()
	posts = Posts.query
	if form.validate_on_submit():
		# Get data from submitted form
		post.searched = form.searched.data
		# Query the Database
		posts = posts.filter(Posts.title.like('%' + post.searched + '%'))
		posts = posts.order_by(Posts.title).all()
		return render_template("search.html",form=form,searched = post.searched,posts = posts)


# Add Post Page
@app.route('/add-post', methods=['GET', 'POST'])
#@login_required
def add_post():
    #if current_user.id == 1:
    form = PostForm()
    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(title=form.title.data, content=form.content.data, poster_id=poster, category=form.category.data)
        # Clear The Form
        form.title.data = ''
        form.content.data = ''
        #form.author.data = ''
        form.category.data = ''
        # Add post data to database
        db.session.add(post)
        db.session.commit()
        # Return a Message
        flash("Blog Post Submitted Successfully!")
    # Redirect to the webpage
    return render_template("add_post.html", form=form)


# Delete posts
@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
	post_to_delete = Posts.query.get_or_404(id)
	id = current_user.id
	if id == 1:
		try:
			db.session.delete(post_to_delete)
			db.session.commit()
			# Return a message
			flash("Blog Post Was Deleted!")
			# Grab all the posts from the database
			posts = Posts.query.order_by(Posts.date_posted)
			return redirect(url_for('admin'))
		except:
			# Return an error message
			flash("Whoops! There was a problem deleting post, try again...")
			# Grab all the posts from the database
			posts = Posts.query.order_by(Posts.date_posted)
			return redirect(url_for('admin'))
	else:
		# Return a message
		flash("You Aren't Authorized To Delete That Post!")		
		# Grab all the posts from the database
		posts = Posts.query.order_by(Posts.date_posted)
		return render_template("posts.html", posts=posts,params=params)


# Edit posts
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
	post = Posts.query.get_or_404(id)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		#post.author = form.author.data
		post.category = form.category.data
		post.content = form.content.data
		# Update Database
		db.session.add(post)
		db.session.commit()
		flash("Post Has Been Updated!")
		return redirect(url_for('post', id=post.id))
	if current_user.id == 1:
		form.title.data = post.title
		#form.author.data = post.author
		form.category.data = post.category
		form.content.data = post.content
		return render_template('edit_post.html', form=form, post=post,params=params)
	else:
		flash("You Aren't Authorized To Edit This Post...")
		posts = Posts.query.order_by(Posts.date_posted)
		return redirect(url_for('post', id=post.id,posts=posts))


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


# Admin Page
@app.route('/admin')
@login_required
def admin():
    id = current_user.id
    if id == 1:
        posts = Posts.query.order_by(Posts.date_posted)
        our_users = Users.query.order_by(Users.date_added)
        return render_template("admin.html", posts=posts, our_users=our_users,params=params)
    else:
        flash("Sorry you must be the Admin to access the Admin Page...")
        return redirect(url_for('profile'))


# Profile Page
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	return render_template("profile.html",params=params)

	# """use this to have update page functionalities in profile page also, will need to have a form in profile for this to work!"""
	
	# form = UserForm()
	# id = current_user.id
	# name_to_update = Users.query.get_or_404(id)
	# if request.method == "POST":
	# 	name_to_update.name = request.form['name']
	# 	name_to_update.email = request.form['email']
	# 	name_to_update.username = request.form['username']
	# 	name_to_update.about_author = request.form['about_author']
	# 	name_to_update.profile_pic = request.files['profile_pic']
	# 	# Grab Image Name
	# 	pic_filename = secure_filename(name_to_update.profile_pic.filename)
	# 	# Set UUID
	# 	pic_name = str(uuid.uuid1()) + "_" + pic_filename
	# 	# Save That Image
	# 	saver = request.files['profile_pic']
		
	# 	# Change it to a string to save to db
	# 	name_to_update.profile_pic = pic_name
	# 	try:
	# 		db.session.commit()
	# 		saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
	# 		flash("User Updated Successfully!")
	# 		return render_template("profile.html", 
	# 			form=form,
	# 			name_to_update = name_to_update)
	# 	except:
	# 		flash("Error!  Looks like there was a problem...try again!")
	# 		return render_template("profile.html", 
	# 			form=form,
	# 			name_to_update = name_to_update)
	# else:
	# 	return render_template("profile.html", 
	# 			form=form,
	# 			name_to_update = name_to_update,
	# 			id = id)


# Update User Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
	form = UserForm()
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		name_to_update.username = request.form['username']
		name_to_update.about_author = request.form['about_author']
		# Check for profile pic
		if request.files['profile_pic']:
			name_to_update.profile_pic = request.files['profile_pic']

			# Grab Image Name
			pic_filename = secure_filename(name_to_update.profile_pic.filename)
			# Set UUID
			pic_name = str(uuid.uuid1()) + "_" + pic_filename
			# Save That Image
			saver = request.files['profile_pic']

			# Change it to a string to save to db
			name_to_update.profile_pic = pic_name
			try:
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
				flash("User Updated Successfully!")
				return render_template("profile.html",form=form,name_to_update = name_to_update,id=id,params=params)
			except:
				flash("Error!  Looks like there was a problem...try again!")
				return render_template("update.html", form=form,name_to_update = name_to_update,params=params)
		else:
			db.session.commit()
			flash("User Updated Successfully!")
			return render_template("profile.html", form=form,name_to_update = name_to_update,id=id,params=params)
	else:
		return render_template("update.html", form=form,name_to_update = name_to_update,id = id,params=params)


# Delete user function
@app.route('/delete/<int:id>')
@login_required
def delete(id):
	# Check logged in id vs. id to delete
	if id == current_user.id or 1:
		user_to_delete = Users.query.get_or_404(id)
		name = None
		form = UserForm()
		try:
			if current_user.id == 1:
				db.session.delete(user_to_delete)
				db.session.commit()
				flash("User Deleted Successfully!!")
				our_users = Users.query.order_by(Users.date_added)
				return redirect("/admin")
			else:
				db.session.delete(user_to_delete)
				db.session.commit()
				flash("User Deleted Successfully!!")
				our_users = Users.query.order_by(Users.date_added)
				return render_template("register.html", 
				form=form,name=name,our_users=our_users,params=params)
		except:
			flash("Whoops! There was a problem deleting user, try again...")
			return render_template("register.html", 
			form=form, name=name, our_users=our_users, params=params)
	else:
		flash("Sorry, you can't delete that user! ")
		return redirect(url_for('profile'))


# Custom Error Pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404


# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500


# Create Password Test Page
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
	email = None
	password = None
	pw_to_check = None
	passed = None
	form = PasswordForm()
	# Validate Form
	if form.validate_on_submit():
		email = form.email.data
		password = form.password_hash.data
		# Clear the form
		form.email.data = ''
		form.password_hash.data = ''
		# Lookup User By Email Address
		pw_to_check = Users.query.filter_by(email=email).first()
		# Check Hashed Password
		passed = check_password_hash(pw_to_check.password_hash, password)
	return render_template("test_pw.html", 
		email = email,
		password = password,
		pw_to_check = pw_to_check,
		passed = passed,
		form = form)


# Contact Section Model
class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_num = db.Column(db.String(20), nullable=False)
    msg = db.Column(db.String(520), nullable=False)
    date = db.Column(db.DateTime, default = datetime.now())

 
# Blog Post Model
class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	content = db.Column(db.Text)
	#author = db.Column(db.String(255))
	date_posted = db.Column(db.DateTime, default=datetime.now())
	category = db.Column(db.String(255), nullable=False)
	# Foreign Key To Link Users (refer to primary key of the user)
	poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))


# User Info Model
class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(120), nullable=False, unique=True)
	about_author = db.Column(db.Text(), nullable=True)
	date_added = db.Column(db.DateTime, default=datetime.now())
	profile_pic = db.Column(db.String(), nullable=True)
	# Do some password stuff!
	password_hash = db.Column(db.String(128))
	# User Can Have Many Posts 
	posts = db.relationship('Posts', backref='poster')

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute!')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	# Create A String
	def __repr__(self):
		return '<Name %r>' % self.name


if __name__=="__main__":
    app.run(debug=True)