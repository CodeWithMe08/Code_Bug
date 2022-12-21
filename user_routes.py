from flask import flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import uuid as uuid
from web_forms import UserForm
import os
from ititialize import app, params
from database import params, db
from models import Users


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

