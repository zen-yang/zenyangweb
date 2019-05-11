from models.weibo import Weibo
from routes import (
    Template,
    current_user,
    html_response,
    login_required,
)
from utils import log


def index(request):
    """
    weibo 首页的路由函数
    """
    u = current_user(request)
    weibos = Weibo.find_all(user_id=u.id)
    log('weiboall', weibos)
    # 替换模板文件中的标记字符串
    body = Template.render('weibo_index.html', weibos=weibos)
    return html_response(body)


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/weibo/index': login_required(index),
    }
    return d
