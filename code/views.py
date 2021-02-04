import json, logging
import os
import platform, random, time
from datetime import datetime

import tornado.web
from tornado.escape import json_encode

from code.func import make_code_or_id
from code.models import db


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info('草拟吗')
        remote_ip = self.request.remote_ip
        data = db.visit.find_one({})

        time_now = datetime.now()
        date = time_now.strftime("%Y-%m-%d")
        visit_num = data['visit_num']
        ip_date = db.visit_list.find({"ip": remote_ip, "date": date})
        if ip_date.count() != 0:
            pass
        else:
            db.visit_list.insert({"ip": remote_ip, "vist_time": time_now, "date": date})
            db.visit.update_one({"visit_num": data['visit_num']}, {"$set":{"visit_num": data['visit_num'] + 1}})
            visit_num += 1

        self.render("index.html", **{"visit_num": visit_num, 'blog_num': data['blog_num']})

    def post(self):
        params = json.loads(self.request.body.decode('utf-8'))

        self.write(json_encode({"code": params}))


class UrlHandler(tornado.web.RequestHandler):
    def get(self, url):
        logging.info(url)
        if url == 'index.html':
            remote_ip = self.request.remote_ip
            data = db.visit.find_one({})

            time_now = datetime.now()
            date = time_now.strftime("%Y-%m-%d")
            visit_num = data['visit_num']
            ip_date = db.visit_list.find({"ip": remote_ip, "date": date})
            if ip_date.count() != 0:
                pass
            else:
                db.visit_list.insert({"ip": remote_ip, "vist_time": time_now, "date": date})
                db.visit.update_one({"visit_num": data['visit_num']}, {"$set":{"visit_num": data['visit_num'] + 1}})
                visit_num += 1

            self.render("index.html", **{"visit_num": visit_num, 'blog_num': data['blog_num']})
        else:
            self.render(url)

    def post(self):
        params = json.loads(self.request.body.decode('utf-8'))

        self.write(json_encode({"code": params}))


class PageHandler(tornado.web.RequestHandler):
    def get(self, url):
        self.render(url)

    def post(self):
        params = json.loads(self.request.body.decode('utf-8'))
        logging.info(params)
        page = params.get('page', 1)
        per_page = params.get('per_page', 10)

        data = db.text.find({}).sort("create_time",-1)
        total_num = data.count()
        res_list = []
        if data:
            for i in data[(int(page) - 1) * per_page:per_page]:
                adict = {}
                adict['title'] = i["title"]
                adict['text_id'] = i["text_id"]
                adict['text'] = i["text"][:30] + '...' if len(i["text"]) > 30 else i["text"]
                adict['create_time'] = i["create_time"].strftime("%Y-%m-%d %H:%M")
                res_list.append(adict)

        self.write(json_encode({"total_num": total_num, "data": res_list}))


class DetailHandler(tornado.web.RequestHandler):
    def get(self, url):
        self.render(url)

    def post(self):
        params = json.loads(self.request.body.decode('utf-8'))
        logging.info(params)
        text_id = params.get('text_id')
        data = db.text.find({"text_id": text_id})
        data = data[0]
        adict = {}
        adict['title'] = data["title"]
        adict['text_id'] = data["text_id"]
        adict['text'] = data["text"]
        adict['create_user'] = data["create_user"]
        adict['type'] = data["type"]
        adict['create_time'] = data['create_time'].strftime("%Y-%m-%d %H:%M")
        adict['up'] = ""
        adict['next'] = ""

        total = db.text.find({}).count()
        if adict['text_id'] != '1':
            adict['up'] = str(int(adict['text_id']) - 1)
        if adict['text_id'] != str(total):
            adict['next'] = str(int(adict['text_id']) + 1)
        self.write(json_encode({"data": adict}))


class UploadImgHandler(tornado.web.RequestHandler):
    def get(self, url):
        self.render(url)

    def post(self):
        imgfile = self.request.files.get('upload')
        path = os.path.abspath(os.getcwd())
        CURRENT_SYSTEM = platform.system()
        if CURRENT_SYSTEM == 'Windows':
            new_dir = path + '\\static\\img\\'
        else:
            new_dir = path + '/static/img/'
        logging.info(new_dir)
        for img in imgfile:
            file_name = make_code_or_id("IMG") + img['filename'].split('.')[1]
            with open(new_dir + file_name, 'wb') as f:
                f.write(img['body'])
        self.write(json_encode({"uploaded": 1, "url": "/wei/img/" + file_name}))


class UploadTextHandler(tornado.web.RequestHandler):
    def get(self, url):
        self.render(url)

    def post(self):
        params = json.loads(self.request.body.decode('utf-8'))
        logging.info(params)
        title = params.get('title')
        text = params.get('text')
        time_now = datetime.now()
        total_text = db.text.find({}).count()
        db.text.insert({"text": text, "title": title, "text_id": str(total_text + 1), "create_time": time_now,
                        "create_user": "wei", "type": "Python"})
        self.write(json_encode({"text_id": str(total_text + 1)}))
