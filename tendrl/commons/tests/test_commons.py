"""
test_commons
----------------------------------

Tests for `commons` module.
"""
import sys

from mock import MagicMock

sys.modules['logging'] = MagicMock()

import tendrl.commons.etcdobj as etcdobj


class PytestEtcdObj(etcdobj.EtcdObj):
    """A simple EtcdObj for testing."""
    __name__ = 'unittesting'
    testingInt = etcdobj.fields.IntField('testingInt')
    testingDict = etcdobj.fields.DictField(
        'testingDict', {'value1': str, 'value2': str})


class TestBridge_commons(object):
    def setup_class(self):
        self.Fields = etcdobj.fields
        self.Etcdobj = etcdobj
