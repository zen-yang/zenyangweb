from models.user import User
from utils import log
from routes import (
    json_response,
    current_user,
    api_login_required,
)

from models.weibo import Weibo
from models.comment import Comment


def all(request):
    weibos = Weibo.all_json()
    # 下面是 weibo 的 all 路由只看到自己 weibo 的方法
    # u = current_user(request)
    # weibos = Weibo.find_all(user_id=u.id)
    # weibos = [w.json() for w in weibos]

    weibo_list = []
    for i in range(len(weibos)):
        weibo_list.append(
            dict(
                id=weibos[i]['id'],
                content=weibos[i]['content'],
                user_id=weibos[i]['user_id'],
                weibo_user=User.find_by(id=weibos[i]['user_id']).username
            )
        )
    weibos = weibo_list

    for weibo in weibos:
        comments = Comment.find_all(weibo_id=weibo['id'])
        comment_list = []
        for i in range(len(comments)):
            comment_list.append(
                dict(
                    id=comments[i].id,
                    content=comments[i].content,
                    user_id=comments[i].user_id,
                    weibo_id=comments[i].weibo_id,
                    comment_user=User.find_by(id=comments[i].user_id).username
                )
            )
        weibo['comments'] = comment_list
    log('allweibos', weibos)
    return json_response(weibos)


def add(request):
    form = request.json()
    u = current_user(request)
    w = Weibo(form)
    w.user_id = u.id
    w.save()
    weibos = w.all_json()

    weibo_list = []
    for i in range(len(weibos)):
        weibo_list.append(
            dict(
                id=weibos[i]['id'],
                content=weibos[i]['content'],
                user_id=weibos[i]['user_id'],
                weibo_user=User.find_by(id=weibos[i]['user_id']).username
            )
        )
    weibos = weibo_list[-1]
    # 把创建好的 weibo 返回给浏览器
    return json_response(weibos)


def delete(request):
    weibo_id = int(request.query['id'])
    Weibo.delete(weibo_id)

    comment_id_list = Comment.find_all(weibo_id=weibo_id)
    for c in comment_id_list:
        Comment.delete(c.id)

    d = dict(
        message="成功删除 weibo和所属评论"
    )

    return json_response(d)


def update(request):
    form = request.json()
    w = Weibo.update(form)
    return json_response(w.json())


def weibo_same_user_required(route_function):

    def f(request):
        u = current_user(request)
        if 'id' in request.query:
            weibo_id = request.query['id']
        else:
            weibo_id = request.json()['id']
            log('what weibo_id', weibo_id)
        w = Weibo.find_by(id=int(weibo_id))

        if w.user_id == u.id:
            return route_function(request)
        else:
            d = dict(
                message="403"
            )
            return json_response(d)

    return f


def comment_add(request):
    form = request.json()
    u = current_user(request)
    c = Comment(form)
    c.user_id = u.id
    c.save()
    comments = c.all_json()

    comment_list = []
    for i in range(len(comments)):
        comment_list.append(
            dict(
                id=comments[i]['id'],
                content=comments[i]['content'],
                user_id=comments[i]['user_id'],
                weibo_id=comments[i]['weibo_id'],
                comment_user=User.find_by(id=comments[i]['user_id']).username
            )
        )
    comments = comment_list[-1]

    return json_response(comments)


def comment_delete(request):
    comment_id = int(request.query['id'])
    Comment.delete(comment_id)
    log('删除的评论id', comment_id)
    d = dict(
        message="成功删除 comment"
    )
    return json_response(d)


def comment_update(request):
    form = request.json()
    log('api comment update form', form)
    c = Comment.update(form)
    return json_response(c.json())


def comment_same_user_required(route_function):

    def f(request):
        u = current_user(request)
        if 'id' in request.query:
            comment_id = request.query['id']
        else:
            comment_id = request.json()['id']
        c = Comment.find_by(id=int(comment_id))

        if c.user_id == u.id:
            return route_function(request)
        else:
            d = dict(
                message="403"
            )
            return json_response(d)

    return f


def comment_delete_required(route_function):

    def f(request):
        u = current_user(request)
        if 'id' in request.query:
            comment_id = request.query['id']
        else:
            comment_id = request.json()['id']
        c = Comment.find_by(id=int(comment_id))
        weibo_id = c.weibo_id
        w = Weibo.find_by(id=int(weibo_id))

        if c.user_id == u.id or w.user_id == u.id:
            return route_function(request)
        else:
            d = dict(
                message="403"
            )
            return json_response(d)

    return f


def route_dict():
    d = {
        '/api/weibo/all': api_login_required(all),
        '/api/weibo/add': api_login_required(add),
        '/api/weibo/delete': api_login_required(weibo_same_user_required(delete)),
        '/api/weibo/update': api_login_required(weibo_same_user_required(update)),
        '/api/comment/add': api_login_required(comment_add),
        '/api/comment/delete': api_login_required(comment_delete_required(comment_delete)),
        '/api/comment/update': api_login_required(comment_same_user_required(comment_update)),
    }
    return d
