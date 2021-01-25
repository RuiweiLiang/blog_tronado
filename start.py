import json, logging
import os

import tornado.ioloop
import tornado.web
from tornado.options import options,define
import tornado.log
import tornado.httpserver
from urls import make_app

# 这里配置的是日志的路径，配置好后控制台的相应信息就会保存到目标路径中。
options.log_file_prefix = os.path.join(os.path.dirname(__file__), 'logs/main.log')

# 格式化日志输出格式
# 默认是这种的：[I 160807 09:27:17 web:1971] 200 GET / (::1) 7.00ms
# 格式化成这种的：[2016-08-07 09:38:01 执行文件名:执行函数名:执行行数 日志等级] 内容消息
class LogFormatter(tornado.log.LogFormatter):
    def __init__(self):
        super(LogFormatter, self).__init__(
            fmt='%(color)s[%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(levelname)s]%(end_color)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

if __name__ == "__main__":
#     app = make_app()
#     app.listen(8080, address="0.0.0.0", xheaders=True)
#     tornado.ioloop.IOLoop.current().start()
    tornado.options.define("port", default="8888", help="run on the port", type=int)  # 设置全局变量port
    tornado.options.parse_command_line()  # 启动应用前面的设置项目
    [i.setFormatter(LogFormatter()) for i in logging.getLogger().handlers]
    http_server = tornado.httpserver.HTTPServer(make_app())
    http_server.listen(tornado.options.options.port,address="0.0.0.0")  # 在这里应用之前的全局变量port
    tornado.ioloop.IOLoop.current().start()  # 启动监听

