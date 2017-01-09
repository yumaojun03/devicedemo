from oslo_db.sqlalchemy import models
import sqlalchemy

from devicedemo.common.db import models as devicedemo_models

Base = devicedemo_models.get_base()


class DeviceDemoBase(models.ModelBase):

    __table_args__ = {'mysql_charset': "utf8",
                      'mysql_engine': "InnoDB"}
    fk_to_resolve = {}

    def save(self, session=None):
        from devicedemo import db

        if session is None:
            session = db.get_session()

        super(DeviceDemoBase, self).save(session=session)

    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            if c.name == 'id':
                continue
            d[c.name] = self[c.name]
        return d

    def _recursive_resolve(self, path):
        obj = self
        for attr in path.split('.'):
            if hasattr(obj, attr):
                obj = getattr(obj, attr)
            else:
                return None
        return obj

    def export_model(self):
        res = self.as_dict()
        for fk, mapping in self.fk_to_resolve.items():
            res[fk] = self._recursive_resolve(mapping)
        return res


class Device(Base, DeviceDemoBase):
    __tablename__ = 'device'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True)
    device_id = sqlalchemy.Column(
        sqlalchemy.String(36),
        nullable=False,
        unique=True)
    name = sqlalchemy.Column(
        sqlalchemy.String(255),
        nullable=False,
        unique=True)
    dtype = sqlalchemy.Column(
        sqlalchemy.String(255),
        nullable=True,
        unique=False)
    vendor = sqlalchemy.Column(
        sqlalchemy.String(255),
        nullable=True,
        unique=False)
    version = sqlalchemy.Column(
        sqlalchemy.String(255),
        nullable=True,
        unique=False)

    def __repr__(self):
        return ('<Device[{uuid}]: '
                'device={device}>').format(
                    uuid=self.device_id,
                    device=self.name)
