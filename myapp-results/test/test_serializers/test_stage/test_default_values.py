import serializers.stage_groups as sz_stage_groups
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
        self.serializer = sz_stage_groups.recursive()['default_values']

    def row_for(self, stage):
        return self.serializer.single_header_for(stage)

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
        self.serializer = sz_stage_groups.recursive()['default_values']

    def row_for(self, stage):
        return self.serializer.single_data_for(stage)

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


class TestStageDataFlat:
    def setUp(self):
        self.stages = my_stages
        self.serializer = sz_stage_groups.flat()['default_values']

    def row_for(self, stage):
        return self.serializer.single_data_for(stage)

    def test_present_past_future(self):
        result = self.row_for(self.stages['present_past_future'])
        assert_equals(result, [
            1/3
        ])

    def test_days_of_week(self):
        result = self.row_for(self.stages['days_of_week'])
        assert_equals(result, [
            1/7
        ])

    def test_seasons_of_year(self):
        result = self.row_for(self.stages['seasons_of_year'])
        assert_equals(result, [
            0
        ])
