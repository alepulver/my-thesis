import unittest
from nose.tools import assert_equals, assert_raises
import samplers
import data_loader


class SimpleSamplerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output = data_loader.DataLoader("examples/tables", "examples/clusters")
        cls.clusters = cls.output.results['present_past_future']
        super(cls)

    def test_returns_correct_keys(self):
        samplerObj = samplers.SimpleSampler(self.clusters, 3)
        assert_equals(set(samplerObj.cluster_names()), set(['1', '2', '3']))

    def test_returns_correct_number_of_elements_when_less(self):
        samplerObj = samplers.SimpleSampler(self.clusters, 3)
        assert_equals(len(samplerObj.sample('1')), 1)
        assert_equals(len(samplerObj.sample('2')), 1)
        assert_equals(len(samplerObj.sample('3')), 1)

    def test_fails_when_asked_for_more_than_available(self):
        samplerObj = samplers.SimpleSampler(self.clusters, 6)

        def func(x):
            return samplerObj.sample(x)

        assert_raises(ValueError, func, '2')


class StratifiedSamplerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output = data_loader.DataLoader("examples/tables", "examples/clusters")
        cls.clusters = cls.output.results['parts_of_day']
        super(cls)

    def test_when_less_than_available(self):
        samplerObj = samplers.StratifiedSampler(self.clusters, 3)
        assert_equals(len(samplerObj.sample('1')), 2)
        assert_equals(len(samplerObj.sample('2')), 1)

    def test_is_sorted_by_center_dist(self):
        samplerObj = samplers.StratifiedSampler(self.clusters, 3)
        center_dist_values = [x['center_dist'] for x in samplerObj.sample('1')]
        assert_equals(center_dist_values[0] <= center_dist_values[1], True)

    def test_when_more_than_available(self):
        samplerObj = samplers.StratifiedSampler(self.clusters, 10)
        assert_equals(len(samplerObj.sample('1')), 3)
        assert_equals(len(samplerObj.sample('2')), 2)