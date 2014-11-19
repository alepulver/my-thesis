import runner
import os
from nose.tools import assert_equals


class TestRunner:
    def setUp(self):
        os.system('mkdir output_test')

    def test_exp_complete(self):
        runner.main(['command', 'examples/results.json', 'output_test'])
        assert_equals('add some tests', False)

    def test_exp_incomplete(self):
        pass

    def test_stages(self):
        pass

    def tearDown(self):
        os.system('rm -rf output_test')
