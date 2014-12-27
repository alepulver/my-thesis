import json
import stages
import serializers.stage_groups as sz_stage_groups
from serializers import groups
from nose.tools import assert_equals

rows = {}
my_stages = {}
stages_rows = []


def setup_module():
    with open("examples/results.json", "r") as fp:
        stages_rows.extend(json.load(fp))

    rows['introduction'] = stages_rows[0]
    rows['parts_of_day'] = stages_rows[1]
    rows['present_past_future'] = stages_rows[2]
    rows['questions_ending'] = stages_rows[3]
    rows['seasons_of_year'] = stages_rows[4]
    rows['timeline'] = stages_rows[5]
    rows['questions_begining'] = stages_rows[6]
    rows['days_of_week'] = stages_rows[7]

    for k in rows.keys():
        my_stages[k] = stages.stage_from(rows[k])


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
            'order_match', 'order_match_reverse'
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
            0, 0.4444444444444444
        ])
