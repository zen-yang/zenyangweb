from models import Model


class Weibo(Model):
    """
    微博类
    """

    def __init__(self, form):
        super().__init__(form)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', None)

    @classmethod
    def update(cls, form):
        weibo_id = int(form['id'])
        w = Weibo.find_by(id=weibo_id)
        w.content = form['content']
        w.save()
        return w
