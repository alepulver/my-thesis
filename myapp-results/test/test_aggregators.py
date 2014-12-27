import aggregators
from nose.tools import assert_equals
import factory

my_stages = None


def setup_module():
    global my_stages
    data = factory.Stages()
    my_stages = data.named_stages()


class TestEvents:
    def test_xxx(self):
        x = aggregators.Events(my_stages['present_past_future'])
        r = x.count_by_type('color')
        assert_equals(r, {'past': 1, 'future': 1, 'present': 3})

    def test_yyy(self):
        x = aggregators.Events(my_stages['parts_of_day'])
        assert_equals(x.order_matching(), 1/3)
        x = aggregators.Events(my_stages['present_past_future'])
        assert_equals(x.order_matching(), 0)


class TestCottle:
    def test_xxx(self):
        x = aggregators.Cottle(my_stages['present_past_future'])
        r = x.relatedness()
        assert_equals(r, -1)

    def test_yyy(self):
        x = aggregators.Cottle(my_stages['present_past_future'])
        r = x.dominance()
        assert_equals(r, {'future': 2, 'present': 4, 'past': 0})
