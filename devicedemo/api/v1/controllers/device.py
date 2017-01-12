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
#
import pecan
from pecan import rest
import six
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan

from devicedemo.api.v1 import types as dd_types
from devicedemo.api.v1.datamodels import device as device_models
from devicedemo.common import policy
from devicedemo.db import api as db_api


class DeviceController(rest.RestController):
    """REST Controller managing device"""


    @wsme_pecan.wsexpose(device_models.Device,
                         dd_types.UuidType(),
                         status_code=200)
    def get_one(self, device_id):
        """Return a device.

        :param device: Uuid of the device to filter on.
        """
        device = db_api.get_instance()
        try:
            device_db = device.get_device(device_id=device_id)
            return device_models.Device(
                **device_db.export_model())
        except db_api.NoSuchDevice as e:
            pecan.abort(404, six.text_type(e))

    @wsme_pecan.wsexpose(device_models.DeviceCollection)
    def get_all(self):
        """Return the list of all device.

        """
        device = db_api.get_instance()
        device_list = []
        devices_obj_list = device.list_devices()
        for device_obj in devices_obj_list:
            device_db = device.get_device(device_id=device_obj.device_id)
            device_list.append(device_models.Device(
                **device_db.export_model()))
        res = device_models.DeviceCollection(devices=device_list)
        return res


    @wsme_pecan.wsexpose(device_models.Device,
                         wtypes.text,
                         wtypes.text,
                         wtypes.text,
                         wtypes.text)
    def post(self, name, dtype=None, vendor=None, version=None):
        """Create a device.

        :param name: Name of the device.
        :param dtype: Type of the device.
        :param vendor: Vendor of the device.
        :param version: Version of the device.
        """
        device = db_api.get_instance()
        try:
            device_db = device.create_device(
                name=name,
                dtype=dtype,
                vendor=vendor,
                version=version)
            pecan.response.location = pecan.request.path_url
            if pecan.response.location[-1] != '/':
                pecan.response.location += '/'
            pecan.response.location += device_db.device_id
            return device_models.Device(
                **device_db.export_model())
        except db_api.DeviceAlreadyExists as e:
            pecan.abort(409, six.text_type(e))
        except db_api.ClientError as e:
            pecan.abort(400, six.text_type(e))

    @wsme_pecan.wsexpose(None,
                         dd_types.UuidType(),
                         wtypes.text,
                         wtypes.text,
                         wtypes.text,
                         wtypes.text)
    def put(self, device_id, name=None, dtype=None, vendor=None, version=None):
        """Update a device.

        :param device_id: device_id of the device to update.
        :param name: Name of the device.
        :param dtype: Type of the device.
        :param vendor: Vendor of the device.
        :param version: Version of the device.
        """
        device = db_api.get_instance()
        try:
            device_db = device.update_device(
                device_id=device_id,
                name=name,
                dtype=dtype,
                vendor=vendor,
                version=version)
            pecan.response.headers['Location'] = pecan.request.path
        except db_api.NoSuchDevice as e:
            pecan.abort(409, six.text_type(e))
        except db_api.ClientError as e:
            pecan.abort(400, six.text_type(e))

    @wsme_pecan.wsexpose(None,
                         dd_types.UuidType(),
                         status_code=204)
    def delete(self, device_id):
        """Delete a device.

        :param device_id: uuid of the device to filter on.
        """
        device = db_api.get_instance()
        try:
            device.delete_device(device_id=device_id)
        except db_api.NoSuchDevice as e:
            pecan.abort(404, six.text_type(e))
