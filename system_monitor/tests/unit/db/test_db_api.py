import mock

from system_monitor.tests.unit import test
from system_monitor.db import api
from system_monitor.db import utils
from system_monitor.db import models


class DBApiTestCase(test.System_MonitorTest):
    def setup(self):
        super(DBApiTestCase, self).setUp()
        print 'test has been setup'

    @mock.patch.object(models, "Agent")
    @mock.patch("sqlalchemy.sql.exists")
    def _test_add_agent(self, mock_exists,
                        mock_agent_model,
                        agent_exists=False):
        mock_session = mock.Mock()
        mock_session.query().scalar.return_value = agent_exists

        api.add_agent(mock.sentinel.agent_name, session=mock_session)

        mock_agent_model.name.__eq__.assert_called_once_with(mock.sentinel.agent_name)
        mock_session.query.assert_called

        if not agent_exists:
            mock_session.add.assert_called_once_with(mock_agent_model.return_value)
            mock_agent_model.assert_called_once_with(name=mock.sentinel.agent_name)

    def test_add_new_agent(self):
        self._test_add_agent()

    def test_add_existing_agent(self):
        self._test_add_agent(agent_exists=True)
