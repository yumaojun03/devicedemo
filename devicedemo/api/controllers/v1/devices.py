# ~*~ coding: utf-8 ~*~
import pecan

from pecan import rest, request
from wsme import types as wtypes

from devicedemo.api import expose


class Device(wtypes.Base):
    uuid = wtypes.text
    name = wtypes.text
    type = wtypes.text
    vendor = wtypes.text
    version = wtypes.text

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "type": self.type,
            "vendor": self.vendor,
            "version": self.version,
        }


class Devices(wtypes.Base):
    devices = [Device]


class RetData(wtypes.Base):
    data = wtypes.text
    error = wtypes.text


class DeviceController(rest.RestController):

    def __init__(self, uuid):
        self.uuid = uuid

    @expose.expose(Device)
    def get(self):
        db_conn = request.db_conn
        device = db_conn.get_device(self.uuid)
        return device

    @expose.expose(Device, body=Device)
    def put(self, device):
        db_conn = request.db_conn
        new_device_obj = db_conn.update_device(device)
        d = Device(**new_device_obj.as_dict())

        return d

    @expose.expose(RetData)
    def delete(self):
        db_conn = request.db_conn
        ret = db_conn.delete_device(self.uuid)
        return RetData(**ret)


class DevicesController(rest.RestController):

    @pecan.expose()
    def _lookup(self, uuid, *remainder):
        return DeviceController(uuid), remainder

    @expose.expose(Devices)
    def get(self):
        # 调用DBHook中创建的Connection实例, 调用所需要的DB API
        db_conn = request.db_conn
        devices = db_conn.list_devices()

        devices_list = []
        for device in devices:
            d = Device()
            d.uuid = device.uuid
            d.name = device.name
            d.type = device.type
            d.vendor = device.vendor
            d.version = device.version

            devices_list.append(d)
        return Devices(devices=devices_list)

    @expose.expose(RetData, body=Device, status_code=201)
    def post(self, device):
        db_conn = request.db_conn
        db_conn.create_device(device)
        ret = RetData(data="create success", error=None)
        return ret
