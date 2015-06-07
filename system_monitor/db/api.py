from system_monitor.db import models
from system_monitor.db import utils
from sqlalchemy.sql import exists


def create_tables():
    models.DeclarativeBase.metadata.create_all(utils.engine)


@utils.ensure_session
def add_agent(name, session=None):
    query = session.query(exists().where(models.Agent.name == name)).scalar()
    if not query:   # add the agent if it doesn't exist in the database
        agent = models.Agent(name=name)
        session.add(agent)


@utils.ensure_session
def add_status(agent_name, curr_status, session=None):
    status = models.Status(curr_status=curr_status, agent_name=agent_name)
    session.add(status)
