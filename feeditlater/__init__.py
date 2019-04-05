import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'fil.db'),
        IMGPATH=os.path.join(app.instance_path, 'imgs'),
        SITE_URL='http://localhost:5000/',
        IMG_URL='http://localhost:5000/images/'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    try:
        os.makedirs(app.config.get("IMGPATH"))
    except OSError:
        pass

    from . import hook, preview, images
    app.register_blueprint(hook.bp)
    app.register_blueprint(preview.bp)
    app.register_blueprint(images.bp(app.config.get("IMGPATH")))


    return app
