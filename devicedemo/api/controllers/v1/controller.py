# ~*~ coding: utf-8 ~*~

from pecan import rest
from wsme import types as wtypes


from devicedemo.api import expose
from devicedemo.api.controllers.v1 import devices as v1_device


class V1Controller(rest.RestController):
    devices = v1_device.DevicesController()

    @expose.expose(wtypes.text)
    def get(self):
        return {"data": "devicedemo v1controller", "error": None}
