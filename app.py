from unicodedata import category
from flask import Flask, flash, render_template,flash,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from web_forms import UserForm,PostForm,LoginForm,PasswordForm,SearchForm
from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
import uuid as uuid
import os

# Create a Flask Instance
app = Flask(__name__)

# Add CKEditor
ckeditor = CKEditor(app)

# SQLite DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# MySQL DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/user01'
# postgres DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qkxekuvvimyqpb:12dbcc3846e4ba7a5c1fa5075ffb93858da3c9ddd73b7c92b9fc7881a159df13@ec2-54-82-205-3.compute-1.amazonaws.com:5432/d7n991c1t52bl5'

'HEROKU_POSTGRESQL_COPPER_URL: postgres://jzldlnekuhbmgt:caf9e6167ea4ac83232fcb9c2b7cc6dd81c48aba2e5249e119e5f8f5cb5b3d71@ec2-44-209-57-4.compute-1.amazonaws.com:5432/d3okvj96ue674l'

app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"

UPLOAD_FOLDER = 'static/imgs/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Initialize The Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

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
@app.route('/')
def index():
	return render_template("index.html")


@app.route('/python')
@login_required
def python():
	# Filter all the posts from the database
    posts = Posts.query.filter_by(category = 'python')
    return render_template("posts.html", posts=posts)


@app.route('/database')
@login_required
def database():
	# Filter all the posts from the database
    posts = Posts.query.filter_by(category = 'database')
    return render_template("posts.html", posts=posts)


@app.route('/selenium')
@login_required
def selenium():
	# Filter all the posts from the database
    posts = Posts.query.filter_by(category = 'selenium')
    return render_template("posts.html", posts=posts)


@app.route('/html-css')
@login_required
def html():
	# Filter all the posts from the database
    posts = Posts.query.filter_by(category = 'html')
    return render_template("posts.html", posts=posts)


@app.route('/django')
@login_required
def django():
	# Filter all the posts from the database
    posts = Posts.query.filter_by(category = 'django')
    return render_template("posts.html", posts=posts)


@app.route('/flask')
@login_required
def flask():
	# Filter all the posts from the database
    posts = Posts.query.filter_by(category = 'flask')
    return render_template("posts.html", posts=posts)


@app.route('/git')
@login_required
def git():
	# Filter all the posts from the database
    posts = Posts.query.filter_by(category = 'git')
    return render_template("posts.html", posts=posts)


# Create posts endpoint
@app.route('/posts')
@login_required
def posts():
	# Grab all the posts from the database
	posts = Posts.query.order_by(Posts.date_posted)
	return render_template("posts.html", posts=posts)


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
		posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
		posts = posts.order_by(Posts.title).all()
		return render_template("search.html",
		 form=form,
		 searched = post.searched,
		 posts = posts)


# Add Post Page
@app.route('/add-post', methods=['GET', 'POST'])
#@login_required
def add_post():
    #if current_user.id == 7:
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
	if id == 7:
		try:
			db.session.delete(post_to_delete)
			db.session.commit()
			# Return a message
			flash("Blog Post Was Deleted!")
			# Grab all the posts from the database
			posts = Posts.query.order_by(Posts.date_posted)
			return render_template("admin.html", posts=posts)
		except:
			# Return an error message
			flash("Whoops! There was a problem deleting post, try again...")
			# Grab all the posts from the database
			posts = Posts.query.order_by(Posts.date_posted)
			return render_template("admin.html", posts=posts)
	else:
		# Return a message
		flash("You Aren't Authorized To Delete That Post!")		
		# Grab all the posts from the database
		posts = Posts.query.order_by(Posts.date_posted)
		return render_template("posts.html", posts=posts)


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
	if current_user.id == 7:
		form.title.data = post.title
		#form.author.data = post.author
		form.category.data = post.category
		form.content.data = post.content
		return render_template('edit_post.html', form=form, post=post)
	else:
		flash("You Aren't Authorized To Edit This Post...")
		posts = Posts.query.order_by(Posts.date_posted)
		return redirect(url_for('post', id=post.id))


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
	return render_template("register.html", 
		form=form,
		name=name,
		our_users=our_users)


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
				flash("Login Successfull!!")
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
    if id == 7:
        posts = Posts.query.order_by(Posts.date_posted)
        our_users = Users.query.order_by(Users.date_added)
        return render_template("admin.html", posts=posts, our_users=our_users)
    else:
        flash("Sorry you must be the Admin to access the Admin Page...")
        return redirect(url_for('profile'))


# Profile Page
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	return render_template("profile.html")

	"""use this to have update page functionalities in profile page also, will nned to have a form in profile for this to work!"""
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
				return render_template("profile.html", 
					form=form,
					name_to_update = name_to_update, id=id)
			except:
				flash("Error!  Looks like there was a problem...try again!")
				return render_template("update.html", 
					form=form,
					name_to_update = name_to_update)
		else:
			db.session.commit()
			flash("User Updated Successfully!")
			return render_template("profile.html", 
				form=form,
				name_to_update = name_to_update, id=id)
	
	else:
		return render_template("update.html", 
				form=form,
				name_to_update = name_to_update,
				id = id)


# Delete user function
@app.route('/delete/<int:id>')
@login_required
def delete(id):
	# Check logged in id vs. id to delete
	if id == current_user.id:
		user_to_delete = Users.query.get_or_404(id)
		name = None
		form = UserForm()
		try:
			db.session.delete(user_to_delete)
			db.session.commit()
			flash("User Deleted Successfully!!")

			our_users = Users.query.order_by(Users.date_added)
			return render_template("register.html", 
			form=form,
			name=name,
			our_users=our_users)
		except:
			flash("Whoops! There was a problem deleting user, try again...")
			return render_template("register.html", 
			form=form, name=name,our_users=our_users)
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

 
# Blog Post Model
class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	content = db.Column(db.Text)
	#author = db.Column(db.String(255))
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
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
	date_added = db.Column(db.DateTime, default=datetime.utcnow)
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