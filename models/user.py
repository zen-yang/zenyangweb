import hashlib
import config
from models import Model
from models.user_role import UserRole


class User(Model):
    def __init__(self, form):
        super().__init__(form)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.role = form.get('role', UserRole.normal)

    @staticmethod
    def guest():

        form = dict(
            role=UserRole.guest,
            password='',
            username='游客',
        )
        u = User(form)
        return u

    def is_guest(self):
        return self.role == UserRole.guest

    def is_admin(self):
        return self.role == UserRole.admin

    @staticmethod
    def salted_password(password, salt=config.salt):
        salted = password + salt
        hashed = hashlib.sha256(salted.encode('ascii')).hexdigest()
        return hashed

    @classmethod
    def login(cls, form):
        salted = cls.salted_password(form['password'])
        u = User.find_by(username=form['username'], password=salted)

        if u is not None:
            result = '登录成功'
            return u, result
        else:
            result = '用户名或者密码错误'
            return User.guest(), result

    @classmethod
    def register(cls, form):
        valid = len(form['username']) > 2 and len(form['password']) > 2
        if valid:
            username = form['username']
            u = cls.find_by(username=username)
            if u is None:
                form['password'] = cls.salted_password(form['password'])
                u = User.new(form)
                result = '注册成功'
                return u, result
            else:
                result = '用户名已被注册'
                return u, result
        else:
            result = '用户名或者密码长度必须大于2'
            return User.guest(), result

    @classmethod
    def update(cls, form):
        user_id = int(form['id'])
        username = form['username']
        password = form['password']
        valid = len(username) > 2 and len(password) > 2

        if valid:
            u = cls.find_by(id=user_id)
            if u is not None:
                u.username = username
                u.password = cls.salted_password(password)
                u.role = form.get('role', u.role)
                u.save()

                result = '更新成功'
            else:
                result = '用户不存在'
        else:
            result = '用户名或者密码长度必须大于2'

        return result
