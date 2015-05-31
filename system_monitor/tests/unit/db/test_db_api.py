import mock

from system_monitor.tests.unit import test
from system_monitor.db import api
from system_monitor.db import utils
from system_monitor.db import models

class mockExists(object): 
    def __init__(self):
        self._scalar = True

    def first(self):  
        return self._first

    def scalar(self): 
        return self._scalar

class mockQuery(object): 
    def __init__(self):
        self._exists = mockExists()
        self._scalar = True

    def scalar(self):  
        return self._scalar

    def exists(self, placeHolder): 
        return self._exists

class mockSession(object):
    def __init__(self):
        self._query = mockQuery()
        self.dirty = []

    def flush(self):
        pass

    def query(self, placeHolder): 
        return self._query

class DBApiTestCase(test.System_MonitorTest):
    def setup(self):
        super(DBApiTestCase, self).setUp()
        print 'test has been setup'

    # @mock.patch.object(utils, 'engine')
    # def _create_tables(self, mock_session_class):
    #     mock_session = api.create_tables()
    #     # with api.create_tables() as mock_session:
    #     # self.assertEqual(mock_session_class.return_value,
    #     #                  mock_session)
    #     mock_session.assert_called_once_with()
    #     # mock_session.close.assert_called_once_with()

    # def test_create_tables(self):
    #     self._create_tables()


    # @mock.patch.object(utils, 'SessionClass')
    def _add_agent(self,name,mock_session_class):
        session = mockSession()
        ps = { 'session' : session }
        mock_session = api.add_agent(name,**ps)
        print mock_session
        # session.query('').exists('')._scalar = True

        self.assertEqual(mock_session_class.return_value, mock_session)

        # mock_session.add.assert_called_once_with(models.Agent(name=name))
        # mock_session.add.assert_called_once_with()

    def test_add_agent(self):
        self._add_agent("test",mock.Mock())



@mock.patch.object(models, "Agent")
@mock.patch("sqlalchemy.sql.exists")
def _test_add_agent(self, mock_exists,
                    mock_agent_model,
                    agent_exists=False):
    mock_session = mock.Mock()
    mock_session.query.scalar.return_value = agent_exists

    api.add_agent(mock.sentinel.agent_name)

    mock_exists.assert_called_once_with()
    mock_agent_model.__eq__.assert_called_once_with(mock.sentinel.agent_name)

    if agent_exists:
        mock_session.add.assert_called_once_with(mock_agent_model.return_value)
    else:
        self.assertFalse(mock_session.add.called)

def test_add_new_agent(self):
    self._test_add_agent()

def test_add_existing_agent(self):
    self._test_add_agent(agent_exists=True)
    