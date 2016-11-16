# ~*~ coding: utf-8 ~*~
from pecan import rest
from wsme import types as wtypes

import wsmeext.pecan as wsme_pecan


class RootController(rest.RestController):

    @wsme_pecan.wsexpose(wtypes.text)
    def get(self):
        return "devicedemo"