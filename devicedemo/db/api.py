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

import abc

from oslo_config import cfg
from oslo_db import api as db_api
import six

_BACKEND_MAPPING = {'sqlalchemy': 'devicedemo.db.sqlalchemy.api'}
IMPL = db_api.DBAPI.from_config(cfg.CONF,
                                backend_mapping=_BACKEND_MAPPING,
                                lazy=True)


def get_instance():
    """Return a DB API instance."""
    return IMPL


class BaseError(Exception):
    """Base class errors."""


class ClientError(BaseError):
    """Base class for client side errors."""


class NoSuchDevice(ClientError):
    """Raised when the device doesn't exist."""

    def __init__(self, device_id=None, name=None):
        super(NoSuchDevice, self).__init__(
            "No such device: %s (UUID: %s)" % (name, device_id))
        self.devicd_id = device_id
        self.name = name


class DeviceAlreadyExists(ClientError):
    """Raised when the device already exists."""

    def __init__(self, device_id, name):
        super(DeviceAlreadyExists, self).__init__(
            "Device %s already exists (UUID: %s)" % (name, device_id))
        self.device_id = device_id
        self.name = name


@six.add_metaclass(abc.ABCMeta)
class Device(object):
    """Base class for state tracking."""

    @abc.abstractmethod
    def get_migration(self):
        """Return a migrate manager.

        """

    @abc.abstractmethod
    def get_device(self, device_id=None, name=None):
        """Retrieve the device object.

        :param device_id: uuid of the device
        :param name: name of the device
        """

    @abc.abstractmethod
    def list_devices(self):
        """Return an list of every devices.

        """

    @abc.abstractmethod
    def create_device(self, name, dtype=None, vendor=None, version=None):
        """Create a new device.

        :param name: Name of the device to create.
        :param dtype: Type of the device to create.
        :param vendor: Vendor of the device to create.
        :param version: Version of the device to create.
        """

    @abc.abstractmethod
    def update_device(self, device_id, name, dtype=None, vendor=None,
                      version=None):
        """Update a device.

        :param device_id: uuid UUID of the device to modify.
        :param name: Name of the device to create.
        :param dtype: Type of the device to create.
        :param vendor: Vendor of the device to create.
        :param version: Version of the device to create.
        """

    @abc.abstractmethod
    def delete_device(self, device_id):
        """Update a device.

        :param device_id: uuid UUID of the device to delete.
        """
