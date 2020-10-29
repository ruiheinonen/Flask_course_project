from flask import render_template, url_for, flash, redirect, Blueprint, request
from flask_login import login_user, current_user, logout_user, login_required
from blogit_main import db
from blogit_main.models import User, BlogPost
from blogit_main.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from blogit_main.users.picture_handler import add_profile_pic, add_bg_picture_pic
from PIL import Image

from blogit_main.blog_posts.views import blog_post

users = Blueprint('users', __name__)

###### REGISTER ###### 
@users.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')
        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)

###### LOGIN ###### 
@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        if user is not None and user.validate_password(form.password.data):
            login_user(user)

            # If user tried to visit a page that requires a login
            # grab the session info  and let flask save that URL as 'next_'.
            next_ = request.args.get('next')

            # Check if that next exists, otherwise we'll go to the welcome page.
            if next_ == None or not next_[0] == '/':
                next_ = url_for('core.index')
            return redirect(next_)

    return render_template('login.html', form=form)

###### LOGOUT ###### 
@users.route('/logout')
def logout():

    logout_user()
    return redirect(url_for('core.index')) # Need to spesicy core.index as we use Blueprint

###### ACCOUNT ###### 

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()
    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            picture = add_profile_pic(form.picture.data, username)
            current_user.profile_image = picture

        if form.bg_picture.data:
            username = current_user.username
            bg_picture = add_bg_picture_pic(form.bg_picture.data, username)
            current_user.bg_image = bg_picture

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User account updated!')
        redirect(url_for('users.account'))

    elif request.method=='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pictures/'+current_user.profile_image)
    bg_image = url_for('static', filename='bg_pictures/'+current_user.bg_image)
    return render_template('account.html', profile_image=profile_image, bg_image=bg_image, form=form)

######  BLOGPOST ###### 

# Dynamic username
@users.route('/<username>')
def user_posts(username):

    # Cyckle trhough the pages
    page = request.args.get('page', 1, type=int)
    # Grab the user or return 404 e.g if user misspells own username 
    user = User.query.filter_by(username=username).first_or_404()
    # author is a backref to Users table in models.py
    # Query all blogposts where the author is particular user, order by date in a descending order
    # paginate allwos to have pages, show 5 blogposts per page by default 
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)
