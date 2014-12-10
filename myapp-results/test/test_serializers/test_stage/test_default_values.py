import json
import stages
import serializers.stage_groups as sz_stage_groups
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
        self.serializer = sz_stage_groups.recursive_single()['default_values']

    def row_for(self, stage):
        return self.serializer.row_header_for(stage)

    def test_present_past_future(self):
        result = self.row_for(type(self.stages['present_past_future']))
        assert_equals(result, [
            'default_size_present', 'default_size_past', 'default_size_future'
        ])

    def test_days_of_week(self):
        result = self.row_for(type(self.stages['days_of_week']))
        assert_equals(result, [
            'default_size_monday', 'default_size_tuesday', 'default_size_wednesday',
            'default_size_thursday', 'default_size_friday', 'default_size_saturday',
            'default_size_sunday'
        ])

    def test_seasons_of_year(self):
        result = self.row_for(type(self.stages['seasons_of_year']))
        assert_equals(result, [
            'default_size_summer', 'default_size_autum',
            'default_size_winter', 'default_size_spring'
        ])


class TestStageData:
    def setUp(self):
        self.stages = my_stages
        self.serializer = sz_stage_groups.recursive_single()['default_values']

    def row_for(self, stage):
        return self.serializer.row_data_for(stage)

    def test_present_past_future(self):
        result = self.row_for(self.stages['present_past_future'])
        assert_equals(result, [
            'no', 'yes', 'no'
        ])

    def test_days_of_week(self):
        result = self.row_for(self.stages['days_of_week'])
        assert_equals(result, [
            'no', 'no', 'no', 'yes', 'no', 'no', 'no'
        ])

    def test_seasons_of_year(self):
        result = self.row_for(self.stages['seasons_of_year'])
        assert_equals(result, [
            'no', 'no', 'no', 'no'
        ])
