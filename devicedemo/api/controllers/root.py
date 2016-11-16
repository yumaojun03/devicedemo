# ~*~ coding: utf-8 ~*~
from pecan import rest
from wsme import types as wtypes

from devicedemo.api import expose
from devicedemo.api.controllers.v1 import controller as v1_controller


class RootController(rest.RestController):
    v1 = v1_controller.V1Controller()

    @expose.expose(wtypes.text)
    def get(self):
        return {"data": "devicedemo"}
