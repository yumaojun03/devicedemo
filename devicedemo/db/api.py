import traceback

from sqlalchemy import orm
from sqlalchemy.orm.exc import NoResultFound
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
        except NoResultFound as e:
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

    def update_device(self, user):
        pass

    def delete_device(self, user):
        pass