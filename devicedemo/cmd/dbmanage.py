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

from oslo_config import cfg

from devicedemo.db import api as db_api
from devicedemo import service

CONF = cfg.CONF

class DBCommand(object):

    def get_migration(self):
        migration = db_api.get_instance().get_migration()
        return migration

    def _version_change(self, cmd):
        revision = CONF.command.revision
        migration = self.get_migration()
        func = getattr(migration, cmd)
        func(revision)

    def upgrade(self):
        self._version_change('upgrade')

    def downgrade(self):
        self._version_change('downgrade')

    def revision(self):
        migration = self.get_migration()
        migration.revision(CONF.command.message, CONF.command.autogenerate)

    def stamp(self):
        migration = self.get_migration()
        migration.stamp(CONF.command.revision)

    def version(self):
        migration = self.get_migration()
        migration.version()


def add_command_parsers(subparsers):
    command_object = DBCommand()

    parser = subparsers.add_parser('upgrade')
    parser.set_defaults(func=command_object.upgrade)
    parser.add_argument('--revision', nargs='?')

    parser = subparsers.add_parser('downgrade')
    parser.set_defaults(func=command_object.downgrade)
    parser.add_argument('--revision', nargs='?')

    parser = subparsers.add_parser('stamp')
    parser.set_defaults(func=command_object.stamp)
    parser.add_argument('--revision', nargs='?')

    parser = subparsers.add_parser('revision')
    parser.set_defaults(func=command_object.revision)
    parser.add_argument('-m', '--message')
    parser.add_argument('--autogenerate', action='store_true')

    parser = subparsers.add_parser('version')
    parser.set_defaults(func=command_object.version)


command_opt = cfg.SubCommandOpt('command',
                                title='Command',
                                help='Available commands',
                                handler=add_command_parsers)

CONF.register_cli_opt(command_opt)


def main():
    service.prepare_service()
    CONF.command.func()
