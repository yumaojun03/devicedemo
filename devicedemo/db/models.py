# ~*~ coding: utf-8 ~*~
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext import declarative
from sqlalchemy import Index


Base = declarative.declarative_base()


class Device(Base):
    """用于记录IOT设备相关属性"""
    __tablename__ = 'device'
    __table_args__ = (
        Index('uuid'),
    )

    id = Column(Integer, primary_key=True)
    uuid = Column(String(255), nullable=False)
    name = Column(String(64), nullable=False, unique=True)
    type = Column(String(255))
    vendor = Column(String(255))
    version = Column(String(64))

    def as_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "type": self.type,
            "vendor": self.vendor,
            "version": self.version,
        }
