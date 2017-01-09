# ~*~ coding: utf-8 ~*~
import traceback

from sqlalchemy import orm
from sqlalchemy.orm import exc as db_exc
from sqlalchemy import create_engine
from devicedemo.db import models as db_models


_ENGINE = None
_SESSION_MAKER = None


def get_engine():
    global _ENGINE
    if _ENGINE is not None:
        return _ENGINE

    # TODO: db的配置应该从配置文件中读取，这里仅为demo
    _ENGINE = create_engine('sqlite:///devicedemo.db')
    db_models.Base.metadata.create_all(_ENGINE)

    return _ENGINE


def get_session_maker(engine):
    global _SESSION_MAKER
    if _SESSION_MAKER is not None:
        return _SESSION_MAKER
    _SESSION_MAKER = orm.sessionmaker(bind=engine)

    return _SESSION_MAKER


def get_session():
    engine = get_engine()
    maker = get_session_maker(engine)
    session = maker()

    return session


class Connection(object):

    def __init__(self):
        pass

    def get_device(self, device_uuid):
        query = get_session().query(db_models.Device).filter_by(uuid=device_uuid)
        try:
            device = query.one()
        except db_exc.NoResultFound as e:
            # No QA
            device = None
            traceback.print_exc()
            print(e)

        return device

    def list_devices(self):
        session = get_session()
        query = session.query(db_models.Device)
        users = query.all()
        return users

    def create_device(self, device):
        session = get_session()
        device_obj = db_models.Device(**device.to_dict())
        try:
            session.add(device_obj)
            session.commit()
        except Exception as e:
            # noqa
            traceback.print_exc()
            print(e)

    def update_device(self, device):
        session = get_session()
        query = session.query(db_models.Device).filter_by(uuid=device.uuid)
        try:
            d = query.one()
            d.name = device.name
            d.type = device.type
            d.vendor = device.vendor
            d.version = device.version
            session.commit()
        except db_exc.NoResultFound as e:
            # No QA
            traceback.print_exc()
            print(e)
            d = None
        return d

    def delete_device(self, uuid):
        session = get_session()
        query = session.query(db_models.Device).filter_by(uuid=uuid)
        ret = {"data": None, "error": None}
        try:
            device = query.one()
            session.delete(device)
            session.commit()
            ret['data'] = "delete device %s success" % uuid
        except db_exc.NoResultFound as e:
            # No QA
            traceback.print_exc()
            print(e)
            ret['error'] = e
        return ret

