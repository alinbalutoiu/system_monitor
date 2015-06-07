import mock

from system_monitor.tests.unit import test
from system_monitor.db import utils


class DBUtilsTestCase(test.System_MonitorTest):
    def setup(self):
        super(DBUtilsTestCase, self).setUp()
        print 'test has been setup'

    @mock.patch.object(utils, 'SessionClass')
    def _test_get_temp_session(self, mock_session_class,
                               raise_exception=False):

        try:
            with utils.get_temp_session() as mock_session:
                self.assertEqual(mock_session_class.return_value,
                                 mock_session)
                if raise_exception:
                    raise Exception('dummy exception')
        except Exception:
            pass
        mock_session.commit.assert_called_once_with()
        mock_session.close.assert_called_once_with()

    def test_get_temp_session(self):
        self._test_get_temp_session()

    def test_get_temp_session_exception(self):
        self._test_get_temp_session(raise_exception=True)
