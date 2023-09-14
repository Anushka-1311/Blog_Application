from flask import render_template, request, Blueprint
from app.models import Post

main = Blueprint('main', __name__)

#Setting route to home page
@main.route("/")
@main.route("/home")
def home():
    # return "<h1>Hello World!</h1>"
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('home.html', posts=posts)
    #Whatever variable name we use as the argument name that we pass in, we will have access to that variable in our template
#We made a database call, and get what we've posted

'''SET ENVIRONMENT VARIABLE
FOR LINUX - export FLASK_APP=app.py
FOR WINDOWS - set FLASK_APP=app.py'''

#Setting route to about page
@main.route("/about")
def about():
    # return "<h1>About Page</h1>"
    return render_template('about.html', title='About')