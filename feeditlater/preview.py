from tinydb import Query

from flask import Blueprint, request

from feeditlater.db import get_db

bp = Blueprint('preview', __name__, url_prefix='/preview')

@bp.route('')
def preview():
    url = request.args.get('url', '')
    articles = Query()
    db = get_db()
    if url:
        article = db.search(articles.url == url)
        if article:
            return article[0]["body"]
        else:
            return "Oops article not found!"
    else:
        return "Oops param required!"

