# zhangguoqing
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo_db import exception
from oslo_db.sqlalchemy import utils
from oslo_utils import uuidutils
import sqlalchemy

from devicedemo import db
from devicedemo.db import api
from devicedemo.db.sqlalchemy import migration
from devicedemo.db.sqlalchemy import models


def get_backend():
    return DeviceManage()


class DeviceManage(api.Device):

    def get_migration(self):
        return migration

    def get_device(self, device_id=None, name=None):
        session = db.get_session()
        try:
            q = utils.model_query(models.Device, session)
            if device_id:
                q = q.filter(models.Device.device_id == device_id)
            if name:
                q = q.filter(models.Device.name == name)
            return q.one()
        except sqlalchemy.orm.exc.NoResultFound:
            raise api.NoSuchDevice(device_id)

    def list_devices(self):
        session = db.get_session()
        q = utils.model_query(models.Device, session)
        res = q.all()
        return res

    def create_device(self, name, dtype=None, vendor=None, version=None):
        session = db.get_session()
        try:
            with session.begin():
                device_db = models.Device(
                    device_id=uuidutils.generate_uuid(),
                    name=name,
                    dtype=dtype,
                    vendor=vendor,
                    version=version)
                session.add(device_db)
            return device_db
        except exception.DBDuplicateEntry:
            device_db = self.get_device(name=name)
            raise api.DeviceAlreadyExists(name, device_db.device_id)

    def update_device(self, device_id, name=None, dtype=None, vendor=None,
                      version=None):
        session = db.get_session()
        try:
            with session.begin():
                q = session.query(models.Device)
                q = q.filter(models.Device.device_id == device_id)
                device_db = q.with_lockmode('update').one()
                if name:
                    device_db.name = name
                if dtype:
                    device_db.dtype = dtype
                if vendor:
                    device_db.vendor = vendor
                if version:
                    device_db.version = version
            return device_db
        except sqlalchemy.orm.exc.NoResultFound:
            raise api.NoSuchDevice(device_id)
        except exception.DBDuplicateEntry:
            device_db = self.get_device(name=name)
            raise api.DeviceAlreadyExists(name, device_db.device_id)

    def delete_device(self, device_id):
        session = db.get_session()
        q = utils.model_query(models.Device, session)
        q = q.filter(models.Device.device_id == device_id)
        r = q.delete()
        if not r:
            raise api.NoSuchDevice(device_id)
