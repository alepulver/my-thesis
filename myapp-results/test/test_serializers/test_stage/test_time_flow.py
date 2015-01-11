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
        self.serializer = sz_stage_groups.recursive()['time_flow']

    def row_for(self, stage):
        return self.serializer.single_data_for(stage)

    def test_present_past_future(self):
        result = self.row_for(self.stages['present_past_future'])
        assert_equals(result, [
            174.44821756853207, 93.72683470581782,
            177.15839320407943, 275.96941084585586,
            8.393389227388845, 182.90713541039256
        ])

    def test_days_of_week(self):
        result = self.row_for(self.stages['days_of_week'])
        assert_equals(result, [
            73.9582950357538, 118.5466463117858,
            109.68501290763176, 158.57828759875275,
            19.2095090681361, 142.81638761942676,
            176.77776637089082, 252.88943882179564,
            49.285966635806915, 128.91742940177008,
            142.78530863311627, 238.5119396801662,
            105.84330949295078, 339.8903901563635
        ])

    def test_seasons_of_year(self):
        result = self.row_for(self.stages['seasons_of_year'])
        assert_equals(result, [
            4.208102986558889, 116.79726771649307,
            176.68836303835425, 86.83769387673973,
            178.3488203344962, 314.101854864633,
            0.7547136405904035, 110.67215302353543
        ])

    def test_parts_of_day(self):
        result = self.row_for(self.stages['parts_of_day'])
        assert_equals(result, [
            236.69850644366272,
            245.23931191187052,
            238.06218164446676
        ])
