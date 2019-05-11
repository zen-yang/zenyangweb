import socket
import _thread

from request import Request
from utils import log

from routes import error

from routes.routes_todo import route_dict as todo_routes
from routes.api_weibo import route_dict as weibo_api
from routes.routes_weibo import route_dict as weibo_routes
from routes.routes_user import route_dict as user_routes
from routes.routes_public import route_dict as public_routes


def response_for_path(request):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    r = {}
    r.update(weibo_api())
    r.update(todo_routes())
    r.update(weibo_routes())
    r.update(user_routes())
    r.update(public_routes())
    response = r.get(request.path, error)
    log('request', request, response)
    return response(request)


def process_request(connection):
    with connection:
        r = connection.recv(1024)
        log('request log:\n <{}>'.format(r))
        r = r.decode()
        # 把原始请求数据传给 Request 对象
        request = Request(r)
        # 用 response_for_path 函数来得到 path 对应的响应内容
        response = response_for_path(request)
        log("response log:\n <{}>".format(response))
        connection.sendall(response)


def run(host, port):
    """
    启动服务器
    """
    log('开始运行于', 'http://{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        s.listen()

        while True:
            connection, address = s.accept()
            log('ip {}'.format(address))
            _thread.start_new_thread(process_request, (connection,))


if __name__ == '__main__':
    config = dict(
        host='localhost',
        port=3000,
    )
    run(**config)
