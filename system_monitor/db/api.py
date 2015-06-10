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
def add_status(agent_name, status, session=None):
    current_status = models.Status(status=status, agent_name=agent_name)
    session.add(current_status)


@utils.ensure_session
def get_status(agent_name, session=None):
    query = session.query(models.Status).options(
                    joinedload(models.Status.agent))
    return query.filter_by(agent_name=agent_name).all()
