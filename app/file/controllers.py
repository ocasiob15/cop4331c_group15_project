import os

from flask import Blueprint, jsonify, url_for, redirect

from app import app

UPLOAD_DIR = app.config['UPLOAD_DIR']

from werkzeug.utils import secure_filename

# get file extension (jpg jpeg png)
def get_ext(filename):
    return filename.rsplit('.', 1)[1].lower()

# check if an extension is in our whitelist, per the
# application configurations
def validate_extension(filename):

    whitelist = app.config['EXTENSION_WHITELIST']

    # no dot in filename. no way to check extension
    if '.' not in filename:
        return False

    # return True if in whitelist
    return get_ext(filename) in whitelist


# utlility validates mulitple files, then save them
def upload(files, path):

    # check if path exists
    if not os.path.isdir(UPLOAD_DIR + path):
        # mkdir
        os.mkdir(UPLOAD_DIR + path, 0o755)

    for file_obj in files:
        filename = secure_filename(file_obj.filename)
        valid = validate_extension(filename)
        if not valid:
            return False
        file_path = UPLOAD_DIR + path + '/' + filename
        file_obj.save(file_path)

    return True

# this function has decorators applied to it by other Blueprints.
# these decorators wrap this function to restrict access based on
# 'ownership' of an entity
def upload_images(files, entity, id):
    upload(files, '/img/' + entity + '/' + str(id))


# this function has decorators applied to it by other Blueprints
# these decorators wrap this function to restrict access based on
# 'ownership' of an entity
def destroy_image(filename, entity, id):

    filename = secure_filename(filename)

    image_path = os.path.join(UPLOAD_DIR, 'img',  entity, str(id), filename)

    # TODO: erase image by filename
    try:
        os.remove(image_path)

    except:
        return False
