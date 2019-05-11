from urllib.parse import unquote_plus

from models.session import Session
from routes import (
    Template,
    current_user,
    html_response,
    random_string,
    redirect,
    login_required,
)

from utils import log
from models.user import User


def login(request):
    """
    登录页面的路由函数
    """
    form = request.form()
    u, result = User.login(form)
    session_id = random_string()

    form = dict(
        session_id=session_id,
        user_id=u.id,
    )
    Session.new(form)

    headers = {
        'Set-Cookie': 'session_id={}; path=/'.format(
            session_id
        )
    }

    return redirect('/user/login/view?result={}'.format(result), headers)


def login_view(request):
    u = current_user(request)
    result = request.query.get('result', '')
    result = unquote_plus(result)

    body = Template.render(
        'user_login.html',
        username=u.username,
        result=result,
    )
    return html_response(body)


def register(request):
    """
    注册页面的路由函数
    """
    form = request.form()

    u, result = User.register(form)
    log('register post', result)

    return redirect('/user/register/view?result={}'.format(result))


def register_view(request):
    result = request.query.get('result', '')
    result = unquote_plus(result)

    body = Template.render('user_register.html', result=result)
    return html_response(body)


def admin(request):
    result = request.query.get('result', '')
    result = unquote_plus(result)

    u = current_user(request)
    us = User.all()

    body = Template.render(
        'user_admin.html',
        username=u.username,
        users=us,
        result=result,
    )
    return html_response(body)


def edit(request):
    user_id = int(request.query['id'])
    u = User.find_by(id=user_id)
    cu = current_user(request)

    body = Template.render(
        'user_edit.html',
        username=cu.username,
        user=u,
    )
    return html_response(body)


def update(request):
    form = request.form()
    result = User.update(form)
    return redirect('/user/admin?result={}'.format(result))


def same_user_required(route_function):
    def f(request):
        query = request.query
        if 'id' in query:
            user_id = int(query['id'])
        else:
            form = request.form()
            user_id = int(form['id'])
        u = current_user(request)

        if u.id == user_id:
            return route_function(request)
        else:
            return redirect('/user/admin?result={}'.format('权限不足'))

    return f


def route_dict():
    r = {
        '/user/login': login,
        '/user/login/view': login_view,
        '/user/register': register,
        '/user/register/view': register_view,
        '/user/admin': login_required(admin),
        '/user/edit': login_required(same_user_required(edit)),
        '/user/update': login_required(same_user_required(update)),
    }
    return r
