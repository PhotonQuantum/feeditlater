from tinydb import Query
import os

from flask import (
    Blueprint, request, Response, current_app
)

from feeditlater.db import get_db, get_imgref
from .parser import Parser, Downloader

bp = Blueprint('hook', __name__, url_prefix='/hook')

@bp.route('/add')
def add():
    db = get_db()
    ref_db = get_imgref()
    def generate(db, url, ref_db, img_path, img_url):
        articles = Query()
        if not url:
            yield "Opps empty url!"
        elif db.search(articles.url == url):
            yield "Oops article exists!"
        else:
            # try:
            yield "Start storing article...\n"
            article = Parser(url)
            yield "Downloading article...\n"
            article.download()
            yield "Parsing article...\n"
            article.parse()
            dict_article = {}
            dict_article["url"] = url
            dict_article["title"] = article.title
            dict_article["authors"] = article.authors
            dict_article["publish_date"] = str(article.publish_date)
            yield "Downloading Pictures...\n"
            downloader = Downloader(article.body, ref_db, Query(), img_path, img_url, url)
            downloader.download()
            dict_article["body"] = downloader.parsed_body
            dict_article["imgs"] = downloader.img_downloaded
            db.insert(dict_article)
            # except:
            #     return "Oops Internal error!"
            yield "OK Article saved."
    return Response(generate(db, request.args.get('url', ''), ref_db, current_app.config["IMGPATH"], current_app.config["IMG_URL"]))

@bp.route('/del')
def delete():
    articles = Query()
    db = get_db()
    db_ref = get_imgref()
    url = request.args.get('url', '')
    if not url:
        return "Opps empty url!"
    if db.search(articles.url == url):
        article = db.search(articles.url == url)[0]
        for img in article["imgs"]:
            img_ref = db_ref.search(Query().hash == img)[0]
            if img_ref["count"] == 1:
                os.remove(os.path.join(current_app.config["IMGPATH"], img))
                db_ref.remove(Query().hash == img)
            else:
                db_ref.update({"count": img_ref["count"] - 1}, Query().hash == img)
        try:
            db.remove(articles.url == url)
        except:
            return "Oops Internal error!"
        return "OK Article removed."
    else:
        return "Oops article doesn't exist!"
