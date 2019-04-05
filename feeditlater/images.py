from flask import Blueprint

def bp(img_path):
    return(Blueprint('images', __name__, static_folder=img_path, static_url_path="/images"))
