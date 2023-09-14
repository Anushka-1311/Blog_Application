from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    #backref allows us to do is, when we have a post we can simply use this author attribute to get the user who created the post
    #lazy argument just define when SQLAlchemy loads the data from the database, so True means that SQLAlchemy will load the data as necessary in one go. With this relationship, we'll be able to simply use this post attribute to get all of the posts created by an individual user.

    def get_reset_token(self,expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    #We tell python not to take self as a parameter and only take token
    @staticmethod
    def verify_reset_token(token):
        s =Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #We are not putting parenthesis after utcnow, to actually run that function or else we want the default to be current time right now. We don't want parenthesis because we want to actually pass in that function as the argument and not the current time.
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

#User model and Post model will have an author in common and both the models have one to many relationships because one user can have multiple posts, but one post can't have multiple author.

#We've used upper case for class in relationship, this is because in the user model we're referencing the actual post class and in the foreign key we're actually referencing the table name and the column name so its the lower case.
