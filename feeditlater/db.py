from tinydb import TinyDB
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = TinyDB(current_app.config['DATABASE'])

    return g.db

def get_imgref():
    if "imgref" not in g:
        g.imgref = TinyDB(current_app.config["DATABASE"]).table("imgref")

    return g.imgref
