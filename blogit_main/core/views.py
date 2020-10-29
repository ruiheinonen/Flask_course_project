from flask import render_template, request, Blueprint
from blogit_main.models import BlogPost

core = Blueprint('core', __name__) # , template_folder='templates', static_folder='static'

@core.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    blog_post = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', blog_posts=blog_post)

@core.route('/info')
def info():
    return render_template('info.html')

