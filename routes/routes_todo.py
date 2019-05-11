from urllib.parse import unquote_plus

from models.todo import Todo
from routes import (
    redirect,
    Template,
    current_user,
    html_response,
    login_required,
)
from utils import log


def index(request):
    result = request.query.get('result', '')
    result = unquote_plus(result)
    u = current_user(request)
    todos = Todo.all()
    # 替换模板文件中的标记字符串
    body = Template.render('todo_index.html', todos=todos, result=result)
    return html_response(body)


def add(request):
    u = current_user(request)
    form = request.form()
    Todo.add(form, u.id)
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/todo/index')


def delete(request):
    todo_id = int(request.query['id'])
    Todo.delete(todo_id)
    return redirect('/todo/index')


def edit(request):
    todo_id = int(request.query['id'])
    t = Todo.find_by(id=todo_id)
    body = Template.render('todo_edit.html', todo=t)
    return html_response(body)


def update(request):
    form = request.form()
    Todo.update(form)
    return redirect('/todo/index')


def same_user_required(route_function):
    def f(request):
        log('same_user_required')
        u = current_user(request)
        if 'id' in request.query:
            todo_id = request.query['id']
        else:
            todo_id = request.form()['id']
        t = Todo.find_by(id=int(todo_id))

        if t.user_id == u.id:
            return route_function(request)
        else:
            return redirect('/todo/index?result={}'.format('权限不足'))

    return f


def admin_required(route_function):
    def f(request):
        u = current_user(request)
        if u.is_admin():
            return route_function(request)
        else:
            return redirect('/todo/index?result={}'.format('非管理员用户'))

    return f


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/todo/add': login_required(add),
        '/todo/delete': login_required(admin_required(delete)),
        '/todo/edit': login_required(same_user_required(edit)),
        '/todo/update': login_required(same_user_required(update)),
        '/todo/index': login_required(index),
    }
    return d
