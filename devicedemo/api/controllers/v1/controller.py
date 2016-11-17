# ~*~ coding: utf-8 ~*~

from pecan import rest
from wsme import types as wtypes


from devicedemo.api import expose
from devicedemo.api.controllers.v1 import users as v1_users


class V1Controller(rest.RestController):
    users = v1_users.UsersController()

    @expose.expose(wtypes.text)
    def get(self):
        return "devicedemo v1controller"
