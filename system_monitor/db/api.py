from system_monitor import constants
from system_monitor.db import models
from system_monitor.db import utils
from sqlalchemy.sql import exists

from sqlalchemy.orm import subqueryload, joinedload


def create_tables():
    models.DeclarativeBase.metadata.create_all(utils.engine)


@utils.ensure_session
def add_agent(name, session=None):
    query = session.query(exists().where(models.Agent.name == name)).scalar()
    if not query:   # add the agent if it doesn't exist in the database
        agent = models.Agent(name=name)
        session.add(agent)


@utils.ensure_session
def add_status(agent_id, curr_status, session=None):
    status = models.Status(curr_status=curr_status, agent_id=agent_id)
    session.add(status)


@utils.ensure_session
def get_agents(session=None):
    query = session.query(models.Agent).\
        options(joinedload(models.Agent.stats)).\
        options(joinedload('stats.agent'))
    return query.order_by(models.Agent.id).all()


@utils.ensure_session
def get_agent(agent_id=None, session=None):
    query = session.query(models.Agent).options(joinedload(models.Agent.stats))
    return query.filter_by(id=agent_id).one()


@utils.ensure_session
def get_stats(agent_id=None, session=None):
    query = session.query(models.Status).options(
                    joinedload(models.Status.agent))
    if agent_id:
        query.filter_by(id=agent_id)
    return query.order_by(models.Status.id).all()  