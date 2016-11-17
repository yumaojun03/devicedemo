# ~*~ coding: utf-8 ~*~
import pecan

from pecan import rest, request
from wsme import types as wtypes

from devicedemo.api import expose


class Device(wtypes.Base):
    id = int
    uuid = wtypes.text
    name = wtypes.text
    type = wtypes.text
    vendor = wtypes.text
    version = wtypes.text


class Devices(wtypes.Base):
    devices = [Device]


class DeviceController(rest.RestController):

    def __init__(self, uuid):
        self.uuid = uuid

    @expose.expose(Device)
    def get(self):
        user_info = {
            'user_id': self.user_id,
            'name': 'Alice',
        }
        return Device(**user_info)

    @expose.expose(Device, body=Device)
    def put(self, user):
        user_info = {
            'user_id': self.user_id,
            'name': user.name,
        }
        return Device(**user_info)

    @expose.expose()
    def delete(self):
        print('Delete user_id: %s' % self.uuid)


class DevicesController(rest.RestController):

    @pecan.expose()
    def _lookup(self, uuid, *remainder):
        return DeviceController(uuid), remainder

    @expose.expose(Devices)
    def get(self):
        # 调用DBHook中创建的Connection实例, 调用所需要的DB API
        db_conn = request.db_conn
        users = db_conn.list_devices()

        devices_list = []
        for user in users:
            u = Device()
            u.id = user.id
            u.user_id = user.user_id
            u.name = user.name
            u.email = user.email
            devices_list.append(u)
        return Devices(users=devices_list)

    @expose.expose(None, body=Device, status_code=201)
    def post(self, user):
        print(user)
