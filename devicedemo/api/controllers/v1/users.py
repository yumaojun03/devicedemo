# ~*~ coding: utf-8 ~*~
from __future__ import print_function, unicode_literals

import pecan

from pecan import rest
from wsme import types as wtypes

from devicedemo.api import expose


class User(wtypes.Base):
    id = int
    user_id = wtypes.text
    name = wtypes.text
    email = wtypes.text


class Users(wtypes.Base):
    users = [User]


class UserController(rest.RestController):

    def __init__(self, user_id):
        self.user_id = user_id

    @expose.expose(User)
    def get(self):
        user_info = {
            'user_id': self.user_id,
            'name': 'Alice',
        }
        return User(**user_info)

    @expose.expose(User, body=User)
    def put(self, user):
        user_info = {
            'user_id': self.user_id,
            'name': user.name,
        }
        return User(**user_info)

    @expose.expose()
    def delete(self):
        print('Delete user_id: %s' % self.user_id)


class UsersController(rest.RestController):

    @pecan.expose()
    def _lookup(self, user_id, *remainder):
        return UserController(user_id), remainder

    @expose.expose(Users)
    def get(self):
        user_info_list = [{
            'id': 1,
            'user_id': 'test_id',
            'name': 'Alice',
            'email': '719118794@qq.com'
            },
            {
            'id': 2,
            'user_id': 'test_id2',
            'name': 'Alice2',
            'email': '719118791@qq.com'
            }
        ]
        users_list = [User(**user_info) for user_info in user_info_list]
        return Users(users=users_list)

    @expose.expose(None, body=User, status_code=201)
    def post(self, user):
        print(user)
