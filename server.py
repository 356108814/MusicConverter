# encoding: utf-8
"""
服务器启动入口
@author Yuriseus
@create 2016-8-1 14:55
"""
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.netutil import bind_sockets
from tornado.options import define, options

import sys

import settings
from application import Application, tornado

define('address', default='localhost', help='run on the given address', type=str)
define('port', default=8891, help='run on the given port', type=int)


def main():
    set_log_setting()
    options.add_parse_callback(set_log_setting)
    options.parse_command_line()
    print_server_info()
    application = Application()
    sockets = bind_sockets(options.port)
    # tornado.process.fork_processes(0)
    server = HTTPServer(application, xheaders=settings.XHEADERS)
    server.add_sockets(sockets)
    IOLoop.current().start()


def set_log_setting():
    """
    设置日志配置，改变tornado默认日志配置
    :return:
    """
    if sys.platform != 'win32':
        options['log_file_prefix'] = 'log'
    options['log_rotate_mode'] = 'time'    # 按时间分割日志，默认按天


def print_server_info():
    print('='*30 + 'server info' + '='*30)
    print('tornado version: %s' % tornado.version)
    print('server started. development server at http://%s:%s/' % (options.address, options.port))


if __name__ == '__main__':
    # 启动带参数
    # python server.py -address 127.0.0.1 -port 8891
    main()


