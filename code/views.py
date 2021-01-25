import json,logging
from datetime import datetime

import tornado.web
from tornado.escape import json_encode

from code.models import db


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info('草拟吗')
        remote_ip = self.request.remote_ip
        cursor = db.cursor()
        cursor.execute("SELECT * from visit")
        data = cursor.fetchone()

        time_now = datetime.now()
        date = time_now.strftime("%Y-%m-%d")
        insert_time = time_now.strftime("%Y-%m-%d %H:%M:%S")

        ip_date = cursor.execute("SELECT ip,date from visit_list where ip='{}' and date='{}'".format(remote_ip,date))
        if ip_date:
            pass
        else:
            # 添加访问列表记录
            cursor.execute(
                "insert into visit_list(ip,vist_time,date) values('{}','{}','{}')".format(remote_ip, insert_time, date))
            # 添加访问人数

            cursor.execute("update visit set visit_num={}".format(str(data[0] + 1)))

        self.render("index.html", **{"visit_num": data[0], 'blog_num': data[1]})
        db.commit()

    def post(self):
        params = json.loads(self.request.body.decode('utf-8'))

        self.write(json_encode({"code": params}))


class UrlHandler(tornado.web.RequestHandler):
    def get(self, url):
        logging.info(url)
        if url == 'index.html':
            remote_ip = self.request.remote_ip
            cursor = db.cursor()
            cursor.execute("SELECT * from visit")
            data = cursor.fetchone()

            time_now = datetime.now()
            date = time_now.strftime("%Y-%m-%d")
            insert_time = time_now.strftime("%Y-%m-%d %H:%M:%S")

            ip_date = cursor.execute("SELECT ip,date from visit_list where ip='{}'".format(remote_ip))
            if ip_date:
                pass
            else:
                # 添加访问列表记录
                cursor.execute(
                    "insert into visit_list(ip,vist_time,date) values('{}','{}','{}')".format(remote_ip, insert_time,
                                                                                              date))
                # 添加访问人数

                cursor.execute("update visit set visit_num={}".format(str(data[0] + 1)))

            self.render("index.html", **{"visit_num": data[0], 'blog_num': data[1]})
            db.commit()
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
        page = params.get('page',1)
        per_page = params.get('per_page',10)
        total_num = 0
        cursor = db.cursor()
        sql = "SELECT title,text_id,text,create_time from text limit {},{};".format(str((int(page) - 1)*per_page), str(per_page))
        cursor.execute(sql)
        data = cursor.fetchall()
        res_list = []
        if data:
            for i in data:
                adict = {}
                adict['title'] = i[0]
                adict['text_id'] = i[1]
                adict['text'] = i[2][:30]+'...' if len(i[2]) > 30 else i[2]
                adict['create_time'] = i[3].strftime("%Y-%m-%d %H:%M")
                res_list.append(adict)

        cursor.execute("select count(text_id) from text")
        total_num = cursor.fetchone()
        self.write(json_encode({"total_num": total_num, "data": res_list}))
        db.commit()


class DetailHandler(tornado.web.RequestHandler):
    def get(self, url):
        self.render(url)

    def post(self):
        params = json.loads(self.request.body.decode('utf-8'))
        logging.info(params)
        text_id = params.get('text_id')
        cursor = db.cursor()
        sql = "SELECT * from text where text_id='{}';".format(text_id)
        logging.info(sql)
        cursor.execute(sql)
        data = cursor.fetchone()
        adict = {}
        adict['title'] = data[0]
        adict['text_id'] = data[2]
        adict['text'] = data[1]
        adict['create_user'] = data[4]
        adict['type'] = data[5]
        adict['create_time'] = data[3].strftime("%Y-%m-%d %H:%M")
        self.write(json_encode({"data": adict}))
        db.commit()