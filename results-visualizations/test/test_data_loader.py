import unittest
from nose.tools import assert_equals
import data_loader


class DataLoaderTest(unittest.TestCase):
    def test_xxx(self):
        results = data_loader.DataLoader("examples/tables", "examples/clusters")
        assert_equals(len(results.results), 6)