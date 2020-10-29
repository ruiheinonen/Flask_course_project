import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__) # , template_folder='templates', static_folder='static'

# Remember you need to set your environment variables at the command line
# when you deploy this to a real website.
# export SECRET_KEY=mysecret
# set SECRET_KEY=mysecret
app.config['SECRET_KEY'] = 'mysecret'

###### DATABASE SETUP ######

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

###### LOGIN CONFIG ######

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'


###### REGISTER BLUEPRINTS ######

from blogit_main.core.views import core
from blogit_main.error_pages.handlers import error_pages
from blogit_main.users.views import users
from blogit_main.blog_posts.views import blog_posts

app.register_blueprint(core) #  url_prefix='/'
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(blog_posts)

