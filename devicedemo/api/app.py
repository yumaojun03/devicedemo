# ~*~ coding: utf-8 ~*~

import os
import pecan

from oslo_config import cfg
from oslo_log import log
from paste import deploy

from devicedemo.api import hooks
from devicedemo.api import config as api_config
from devicedemo.api import middleware
from devicedemo.common import defaults as common_config
import devicedemo.conf
from devicedemo.common.i18n import _LI

CONF = devicedemo.conf.CONF

LOG = log.getLogger(__name__)


def get_pecan_config():
    filename = api_config.__file__.replace('.pyc', '.py')
    return pecan.configuration.conf_from_file(filename)


def setup_app(config=None):
    if not config:
        config = get_pecan_config()

    app_hooks = [hooks.DBHook()]
    app_conf = dict(config.app)
    common_config.set_config_defaults()

    app = pecan.make_app(
        app_conf.pop('root'),
        logging=getattr(config, 'logging', {}),
        hooks=app_hooks,
        wrap_app=middleware.ParsableErrorMiddleware,
        **app_conf
    )

    return app


def load_app():
    cfg_file = None
    cfg_path = CONF.api.api_paste_config
    if not os.path.isabs(cfg_path):
        cfg_file = CONF.find_file(cfg_path)
    elif os.path.exists(cfg_path):
        cfg_file = cfg_path

    if not cfg_file:
        raise cfg.ConfigFilesNotFoundError([CONF.api.api_paste_config])
    LOG.info(_LI("Full WSGI config used: %s"), cfg_file)
    return deploy.loadapp("config:" + cfg_file)


def app_factory(global_config, **local_conf):
    return setup_app()
