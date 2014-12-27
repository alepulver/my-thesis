import serializers.stage_groups as sz_stage_groups
from nose.tools import assert_equals
import factory

my_stages = None


def setup_module():
    global my_stages
    data = factory.Stages()
    my_stages = data.named_stages()


class TestStageData:
    def setUp(self):
        self.stages = my_stages
        self.serializer = sz_stage_groups.recursive()['events']

    def row_for(self, stage):
        return self.serializer.single_data_for(stage)

    def test_present_past_future(self):
        result = self.row_for(self.stages['present_past_future'])
        assert_equals(result, [
            145, 41149, 3, 98, 41, 3,
            39, 7429, 0, 38, 0, 1,
            59, 16669, 2, 24, 32, 1
        ])

    def test_days_of_week(self):
        result = self.row_for(self.stages['days_of_week'])
        assert_equals(result, [
            44, 13261, 2, 14, 27, 1,
            28, 8103, 0, 0, 27, 1,
            27, 36740, 0, 18, 8, 1,
            23, 6693, 1, 21, 0, 1,
            42, 16068, 0, 23, 17, 2,
            22, 8216, 0, 0, 20, 2,
            49, 11159, 0, 1, 47, 1
        ])

    def test_seasons_of_year(self):
        result = self.row_for(self.stages['seasons_of_year'])
        assert_equals(result, [
            47, 9238, 0, 0, 46, 1,
            46, 17288, 0, 7, 38, 1,
            30, 9679, 0, 6, 23, 1,
            45, 9440, 1, 0, 43, 1
        ])

    def test_parts_of_day(self):
        result = self.row_for(self.stages['parts_of_day'])
        assert_equals(result, [
            35, 15976, 1, 6, 26, 2,
            28, 15944, 0, 7, 20, 1,
            38, 9231, 1, 0, 37, 0
        ])

    def test_timeline(self):
        result = self.row_for(self.stages['timeline'])
        assert_equals(result, [
            29, 9511, 0, 29,
            16, 6050, 0, 16,
            30, 7386, 0, 30,
            34, 8726, 0, 34,
            39, 5706, 1, 38,
            30, 4904, 0, 30,
            57, 27214, 1, 56,
            34, 6489, 0, 34,
            11, 4624, 0, 11
        ])
