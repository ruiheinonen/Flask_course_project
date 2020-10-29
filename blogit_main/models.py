# no need for puppy_company_blog_main.models as we import from init 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from blogit_main import db, login_manager
# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()

# The user_loader decorator allows flask-login to load the current user and grab their id.
# Essentially allows to do some stuff if user is authenticated
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    # Images as string bc it's a link to image file that user uplodas. Also set default pics
    profile_image = db.Column(db.String(64), nullable=False, default='default_profile.jpg')
    bg_image = db.Column(db.String(64), nullable=False, default='default_bg_image.jpg')
    # Each email has to be unique, index=True allows to make the column into an index in SQL
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    # Set relationship between User and BlogPost
    posts = db.relationship('BlogPost', backref='author', lazy=True)

    # Make an instance of an user, hash password
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    # Check that pasword provided at logged in when hashed matches currently hashed password
    # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Print simple representation when logged in 
    def __repr__(self):
        return f'Username: {self.username}'

class BlogPost(db.Model):

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    # Connects BlogPost to the User. nullable=False - every BlogPosts must have user_id associated with it
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # nullable=False - every BlogPosts must have latest publish date
    # default=datetime.utcnow - when someone publishes a post it automatiaclly gets a assigned with the date of publication
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(256), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id 

    def __repr__(self):
        return f'Post id: {self.id} -- Date: {self.date}'