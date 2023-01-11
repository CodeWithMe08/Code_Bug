from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from web_forms import PostForm, SearchForm
import uuid as uuid
import math
from sqlalchemy.sql import func
from database import params, db
from models import Posts
from initial import app, params


@app.route('/posts/<paths>')
@login_required
def python(paths):
	# Filter all the posts from the database
	posts = Posts.query.filter_by(category = paths).all()

	last = math.ceil(len(posts)/int(params['no_of_posts']))
	page = request.args.get('page')
	if (not str(page).isnumeric()):
		page = 1
	page = int(page)
	posts = posts[(page-1)*int(params['no_of_posts']):(page-1)*int(params['no_of_posts'])+ int(params['no_of_posts'])]
	if page == 1:
		prev = "#"
		next = f"/posts/{paths}?page="+ str(page+1)
	elif page == last:
		prev = f"/posts/{paths}?page="+ str(page-1)
		next = "#"
	else:
		prev = f"/posts/{paths}?page="+ str(page-1)
		next = f"/posts/{paths}?page="+ str(page+1)
		
	return render_template('posts.html', params=params, posts=posts, prev=prev, next=next)


# All posts in a random way
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


# post endpoint
@app.route('/posts/<int:id>')
@login_required
def post(id):		
	max_id = 0
	min_id = float('inf')
	post = Posts.query.get_or_404(id)
	posts = Posts.query.filter_by().all()
		
	for p in posts:
		if p.id > max_id:
			max_id = p.id
		if p.id < min_id:
			min_id = p.id
	
	if post.id == min_id:
		prev = "#"
		nexts = f"/posts/{int(id+1)}"
	elif post.id == max_id:
		prev = f"/posts/{int(id-1)}"
		nexts = "#"
	else:
		prev = f"/posts/{int(id-1)}"
		nexts = f"/posts/{int(id+1)}"
	return render_template('post.html', params=params, post=post, prev=prev, nexts=nexts)


# Search Function
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


# Passing Stuff To Navbar
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

