# ~*~ coding: utf-8 ~*~
from pecan import hooks
from devicedemo.db import api as db_api


class DBHook(hooks.PecanHook):
    """
    在每个请求进来的时候实例化一个db的Connection对象，
    然后在controller代码中我们可以直接使用这个Connection实例
    """

    def before(self, state):
        state.request.db_conn = db_api.Connection()


