import experiments
import serializers.experiment as sz_exp
from nose.tools import assert_equals
import factory

my_stages = None


def setup_module():
    global my_stages
    data = factory.Stages()
    my_stages = data.named_stages()


class TestExperimentHeader:
    def setUp(self):
        self.serializer = sz_exp.Summary()

    def test_row(self):
        result = self.serializer.header_for(None)

        assert_equals(len(result), 6)
        assert_equals(result, [
            'id', 'num_stages', 'start_time',
            'duration', 'is_complete', 'size_in_bytes'
        ])


class TestExperimentData:
    def setUp(self):
        self.serializer = sz_exp.Summary()

    def test_row(self):
        self.experiment = experiments.experiments_from(my_stages.values())[0]
        result = self.serializer.data_for(self.experiment)

        assert_equals(len(result), 6)
        assert_equals(result, [
            'a7e32988-9e4b-4a2d-bbb2-a35798e7e8f1', 8, 1410966188680,
            556956, True, 131271
        ])
