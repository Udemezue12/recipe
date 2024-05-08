

import os
from PIL import Image
from flask import current_app
import secrets


def add_profile_pic(pic_upload, username):
    filename = pic_upload.username
    ext_type = filename.split('.')[-1]
    storage_filename = f"{username}.{ext_type}"

    filepath = os.path.join(current_app.root_app,
                            '/static/profile_pics', storage_filename)

    output_size = (200, 200)

    with Image.open(pic_upload) as pic:

        pic.thumbnail(output_size)
        pic.save(filepath)

    return storage_filename


def delete_profile_pic(filename):
    filepath = os.path.join(current_app.root_path,
                            '/static/profile_pics', filename)
    try:
        os.remove(filepath)
        return True
    except FileNotFoundError:
        return False


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, 'static', 'recipe_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn
