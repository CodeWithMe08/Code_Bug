from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from web_forms import PostForm, SearchForm
import uuid as uuid
import math
from sqlalchemy.sql import func
from ititialize import app, params
from database import params, db
from models import Posts

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
	posts = Posts.query.filter_by(category = 'framework')
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


# Pass Stuff To Navbar
@app.context_processor
def base():
	form = SearchForm()
	return dict(form=form)


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


