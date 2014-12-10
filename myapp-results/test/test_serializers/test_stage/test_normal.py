import json
import stages
import serializers.stage.normal as sz_normal
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
        self.sz_flat = sz_normal.FlatHeader()
        self.sz_recursive = sz_normal.RecursiveHeader()

    def common_row(self):
        return self.sz_flat.common_row()

    def flat_row_for(self, stage):
        return stage.visit_class(self.sz_flat)

    def recursive_row_for(self, stage):
        return stage.visit_class(self.sz_recursive)

    def test_common(self):
        result = self.common_row()
        assert_equals(result, ['time_start', 'time_duration', 'size_in_bytes'])

    def test_introduction(self):
        result = self.flat_row_for(stages.Introduction)
        assert_equals(result, ['ip_address', 'user_agent', 'participant', 'local_id'])

    def test_parts_of_day(self):
        result = self.recursive_row_for(stages.PartsOfDay)
        assert_equals(result, [
            'rotation', 'size', 'color',
        ])

    def test_questions_ending(self):
        result = self.flat_row_for(stages.QuestionsEnd)
        assert_equals(result, [
            'represents_time', 'cronotype',
            'forced_size', 'forced_color', 'forced_position'
        ])

    def test_seasons_of_year(self):
        result = self.recursive_row_for(stages.SeasonsOfYear)
        assert_equals(result, [
            'center_x', 'center_y', 'size_x', 'size_y', 'color'
        ])

    def test_timeline_flat(self):
        result = self.flat_row_for(stages.Timeline)
        assert_equals(result, [
            'line_rotation', 'line_length', 'button_order'
        ])

    def test_timeline_recursive(self):
        result = self.recursive_row_for(stages.Timeline)
        assert_equals(result, [
            'position'
        ])

    def test_questions_begining(self):
        result = self.flat_row_for(stages.QuestionsBegin)
        assert_equals(result, ['name', 'age', 'sex'])

    def test_days_of_week(self):
        result = self.recursive_row_for(stages.DaysOfWeek)
        assert_equals(result, [
            'center_x', 'center_y', 'size_y', 'color'
        ])


class TestStageData:
    def setUp(self):
        self.stages = my_stages
        self.sz_flat = sz_normal.FlatData()
        self.sz_recursive = sz_normal.RecursiveData()

    def common_row_for(self, stage):
        return self.sz_flat.common_row_for(stage)

    def flat_row_for(self, stage):
        return stage.visit(self.sz_flat)

    def recursive_row_for(self, stage):
        return stage.visit(self.sz_recursive)

    def test_common(self):
        result = self.common_row_for(self.stages['introduction'])
        assert_equals(result, [1410966188680, 55448, 423])

    def test_introduction(self):
        result = self.flat_row_for(self.stages['introduction'])
        assert_equals(result, [
            '200.0.255.1',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/37.0.2062.120 Safari/537.36',
            '324',
            'ISc_wgAqEj4ckmtm4Ir2TDw-Nfzniy0ONXF_U6kPyv1'
        ])

    def test_parts_of_day(self):
        result = self.recursive_row_for(self.stages['parts_of_day'])
        assert_equals(result, [
            'rotation', 'size', 'color'
        ])

    def test_questions_ending(self):
        result = self.flat_row_for(self.stages['questions_ending'])
        assert_equals(result, ['much', 'nocturna', 0.7, 0.3, 0.7])

    def test_seasons_of_year(self):
        result = self.recursive_row_for(self.stages['seasons_of_year'])
        assert_equals(result, [
            'center_x', 'center_y', 'size_x', 'size_y', 'color'
        ])

    def test_timeline_flat(self):
        result = self.flat_row_for(self.stages['timeline'])
        assert_equals(result, [
            44.84884095673553, 724.8023584003396, 'chronological',
        ])

    def test_timeline_recursive(self):
        result = self.recursive_row_for(self.stages['timeline'])
        assert_equals(result, [
            'position'
        ])

    def test_questions_begining(self):
        result = self.flat_row_for(self.stages['questions_begining'])
        assert_equals(result, ['Mora', '32', 'female'])

    def test_days_of_week(self):
        result = self.recursive_row_for(self.stages['days_of_week'])
        assert_equals(result, [
            'center_x', 'center_y', 'size_y', 'color'
        ])
