from flask import flash, render_template, redirect, url_for
from flask_login import login_required, current_user
import uuid as uuid
from ititialize import app, params
from database import params
from models import Users, Posts

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
