import os
import secrets
from flask_mail import Message
from flask import url_for, current_app
from PIL import Image
from app import mail

#code to save picture to the file folder
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    #resizing image before saving
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

#Code for sending email
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='qa_amishra@outlook.com', recipients=[user.email])
    msg.body = f'''To reset your password visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}

    If you did not make this request then simply ignore this email and no change will be made
    '''
    #_external = True is used inorder to get an absolute url rather than a relative url, because relative url are fine within our application but the link in the email has to have complete domain
    mail.send(msg)