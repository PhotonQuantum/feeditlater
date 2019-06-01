from newspaper import Article
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib.request
import os
import hashlib

class Parser():
    def __init__(self, url, lang="zh"):
        self.authors = None
        self.title = None
        self.publish_date = None
        self.body = None
        self.imgs = None
        self.parser = Article(url, language=lang, keep_article_html=True)
    def download(self):
        self.parser.download()
    def parse(self):
        self.parser.parse()
        self.authors = self.parser.authors
        self.title = self.parser.title
        self.publish_date = self.parser.publish_date
        self.body = self.parser.article_html
        self.imgs = self.parser.imgs

class Downloader():
    def __init__(self, body, img_ref_db, query, img_dir, url_prefix, src_url):
        self.body = body
        self.img_ref_db = img_ref_db
        self.query = query
        self.img_dir = img_dir
        self.url_prefix = url_prefix
        self.src_url = src_url
        self.parsed_body = ""
        self.img_downloaded = []
    def __download__(self, img):
        print(img)
        img_tmp = urllib.request.urlopen(img).read()
        h = hashlib.new("md5")
        h.update(img_tmp)
        hash_img = h.hexdigest()
        ext = os.path.splitext(img)[-1]
        ref = self.img_ref_db.search(self.query.hash == hash_img + ext)
        if ref:
            self.img_ref_db.update({"count": ref[0]["count"] + 1}, self.query.hash == hash_img + ext)
        else:
            with open(os.path.join(self.img_dir, hash_img + ext), mode="wb") as f:
                f.write(img_tmp)
            self.img_ref_db.insert({"hash": hash_img + ext, "count": 1})
        return os.path.join(self.img_dir, hash_img + ext), hash_img + ext
    def download(self):
        self.img_downloaded = []
        body = self.body
        bs = BeautifulSoup(body, "lxml")
        for img in bs.findAll("img"):
            try:
                src = img["src"]
                fp, fn = self.__download__(urljoin(self.src_url, src))
                self.img_downloaded.append(fn)
                img["src"] = urljoin(self.url_prefix, fn)
            except KeyError:
                img.decompose()
        self.parsed_body = str(bs)
