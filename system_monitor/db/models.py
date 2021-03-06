from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.types import PickleType

from system_monitor.db import utils


class BaseModel(object):
    id = Column(Integer, primary_key=True)

    def save():
        session = utils.get_new_session()
        with session.begin():
            session.add(self)

    def _to_dict(self):
        _dict = {col.name: getattr(self, col.name)
                 for col in self.__table__.columns}
        return _dict


DeclarativeBase = declarative_base(cls=BaseModel)


def ModelJsonEncoder(obj):
    if isinstance(obj, BaseModel):
        return obj._to_dict()
    else:
        return json.dumps(obj)


class Agent(DeclarativeBase):
    __tablename__ = 'agents'

    name = Column(String(32))

    def __str__(self):
        return 'Agent: Name: %s' % self.name

    def __repr__(self):
        return str(self)


class Status(DeclarativeBase):
    __tablename__ = 'stats'

    status = Column(PickleType)

    agent_name = Column(ForeignKey('agents.name'))

    agent = relationship("Agent", 
                         backref=backref('stats'), 
                         order_by='Agent.name')

    def __str__(self):
        return '%(agent)s: %(status)s' % {'agent': self.agent.name,
                                               'status': self.status}

    def __repr__(self):
        return str(self)
