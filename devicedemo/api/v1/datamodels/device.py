# -*- coding: utf-8 -*-
# Copyright 2014 Objectif Libre
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# @author: Stéphane Albert
#
from wsme import types as wtypes

from devicedemo.api.v1 import types as ck_types


class Device(wtypes.Base):
    """Type describing a device.

    """

    device_id = wtypes.wsattr(ck_types.UuidType(), mandatory=False)
    """Uuid of the service."""

    name = wtypes.text
    """Name of the device."""

    dtype = wtypes.text
    """Type of the device."""

    vendor = wtypes.text
    """Vendor of the device."""

    version = wtypes.text
    """Version of the device."""


    def to_json(self):
        res_dict = {'deivce_id': self.device_id,
                    'name': self.name,
                    'dtype': self.dtype,
                    'vendor': self.vendor,
                    'version': self.version}
        return res_dict

    @classmethod
    def sample(cls):
        sample = cls(device_id='faf7404e-1d9a-47d2-bc49-48569ad5ed6e',
                     name='device-001',
                     dtype='device-type-001',
                     vendor='tongfangcloud',
                     version='device-version-001')
        return sample


class DeviceCollection(wtypes.Base):
    """Type describing a list of devices.

    """

    devices = [Device]
    """List of devices."""

    @classmethod
    def sample(cls):
        sample = Device.sample()
        return cls(devices=[sample])
