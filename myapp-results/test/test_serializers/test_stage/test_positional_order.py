import serializers.stage_groups as sz_stage_groups
from serializers import groups
from nose.tools import assert_equals
import factory

my_stages = None


def setup_module():
    global my_stages
    data = factory.Stages()
    my_stages = data.named_stages()


class TestStageHeader:
    def setUp(self):
        self.stages = my_stages
        self.serializer = groups.SingleWrapper(sz_stage_groups.flat()['positional_order'])

    def row_for(self, stage):
        return self.serializer.header_for(stage)

    def test_present_past_future(self):
        result = self.row_for(type(self.stages['present_past_future']))
        assert_equals(result, [
            'order_x', 'order_y'
        ])

    def test_parts_of_day(self):
        result = self.row_for(type(self.stages['parts_of_day']))
        assert_equals(result, [
            'order'
        ])

    def test_days_of_week(self):
        result = self.row_for(type(self.stages['days_of_week']))
        assert_equals(result, [
            'order_x'
        ])

    def test_timeline(self):
        result = self.row_for(type(self.stages['timeline']))
        assert_equals(result, [
            'order', 'order_match'
        ])


class TestStageData:
    def setUp(self):
        self.stages = my_stages
        self.serializer = groups.SingleWrapper(sz_stage_groups.flat()['positional_order'])

    def row_for(self, stage):
        return self.serializer.data_for(stage)

    def test_present_past_future(self):
        result = self.row_for(self.stages['present_past_future'])
        assert_equals(result, [
            'past_present_future', 'future_present_past'
        ])

    def test_parts_of_day(self):
        result = self.row_for(self.stages['parts_of_day'])
        assert_equals(result, [
            'counterclockwise'
        ])

    def test_days_of_week(self):
        result = self.row_for(self.stages['days_of_week'])
        assert_equals(result, [
            'not_ordered'
        ])

    def test_timeline(self):
        result = self.row_for(self.stages['timeline'])
        assert_equals(result, [
            'right_left', 0.8888888888888888
        ])
