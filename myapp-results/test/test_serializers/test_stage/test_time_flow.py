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
            -16.061908333987468, 93.72683470581782, -185.551782431468,
            -7.668519106598656, 182.90713541039256, 8.39338922738881,
            169.48987409748057, 275.96941084585586, 177.15839320407923
        ])

    def test_days_of_week(self):
        result = self.row_for(self.stages['days_of_week'])
        assert_equals(result, [
            -174.4955588533465, 118.5466463117858, -254.15669050704923,
            -100.53726381759269, 158.57828759875275, 73.9582950357538,
            9.147749090039088, 142.81638761942676, 109.68501290763177,
            -10.061759978097026, 252.88943882179564, -19.209509068136114,
            173.1604736510121, 128.91742940177008, 183.22223362910913,
            -137.55355971318102, 238.5119396801662, -310.7140333641931,
            79.66113165370274, 339.8903901563635, 217.21469136688376
        ])

    def test_seasons_of_year(self):
        result = self.row_for(self.stages['seasons_of_year'])
        assert_equals(result, [
            -99.08569190292243, 116.79726771649307, 0.7547136405901383,
            -94.87758891636342, 86.83769387673973, 4.208102986559012,
            81.81077412199089, 314.101854864633, 176.6883630383543,
            -99.84040554351257, 110.67215302353543, -181.65117966550343
        ])

    def test_parts_of_day(self):
        result = self.row_for(self.stages['parts_of_day'])
        assert_equals(result, [
            123.30149355633728,
            114.76068808812948,
            121.93781835553324
        ])
