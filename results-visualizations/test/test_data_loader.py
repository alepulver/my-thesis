import unittest
from nose.tools import assert_equals
import data_loader


class DataLoaderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output = data_loader.DataLoader("examples/tables", "examples/clusters")
        super(cls)

    def test_loads_all_stages(self):
        assert_equals(len(self.output.results), 5)

    def test_loads_center_dist(self):
        clusters = self.output.results['present_past_future']
        element = clusters['2'][0]
        assert_equals(element['center_dist'], 2.84872231712825)

    def test_present_past_future(self):
        clusters = self.output.results['present_past_future']
        assert_equals(len(clusters), 3)
        assert_equals(len(clusters['1']), 3)
        assert_equals(len(clusters['2']), 1)
        assert_equals(len(clusters['3']), 1)

    def test_seasons_of_year(self):
        clusters = self.output.results['seasons_of_year']
        assert_equals(len(clusters), 4)
        assert_equals(len(clusters['1']), 2)
        assert_equals(len(clusters['2']), 1)
        assert_equals(len(clusters['3']), 1)
        assert_equals(len(clusters['4']), 1)

    def test_days_of_week(self):
        clusters = self.output.results['days_of_week']
        assert_equals(len(clusters), 2)
        assert_equals(len(clusters['1']), 4)
        assert_equals(len(clusters['2']), 1)

    def test_parts_of_day(self):
        clusters = self.output.results['parts_of_day']
        assert_equals(len(clusters), 2)
        assert_equals(len(clusters['1']), 3)
        assert_equals(len(clusters['2']), 2)

    def test_timeline(self):
        clusters = self.output.results['timeline']
        assert_equals(len(clusters), 3)
        assert_equals(len(clusters['1']), 1)
        assert_equals(len(clusters['2']), 3)
        assert_equals(len(clusters['3']), 1)