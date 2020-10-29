import os 
from PIL import Image
from flask import url_for, current_app

def add_profile_pic(pic_upload, username):

    filename = pic_upload.filename
    # mypic.png -> png
    extension_type = filename.split('.')[-1]
    # save profile pic as username.extension_type
    storage_filename = str(username) + '.' + extension_type
    filepath = os.path.join(current_app.root_path, 'static/profile_pictures', storage_filename)

    output_size = (200, 200)
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)  
    pic.save(filepath)

    return storage_filename

def add_bg_picture_pic(pic_upload, username):

    filename = pic_upload.filename
    # mypic.png -> png
    extension_type = filename.split('.')[-1]
    # save profile pic as username.extension_type
    storage_filename = str(username) + '.' + extension_type
    filepath = os.path.join(current_app.root_path, 'static/bg_pictures', storage_filename)

    output_size = (800, 400)
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)  
    pic.save(filepath)

    return storage_filename