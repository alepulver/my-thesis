import json
import experiments
import stages
import serializers
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
        self.serializer = serializers.StageHeader()

    def test_common(self):
        result = self.serializer.common_row_for(self.stages['introduction'])
        assert_equals(result, ['experiment_id', 'time_start', 'time_duration', 'size_in_bytes'])

    def test_introduction(self):
        result = self.serializer.row_for(self.stages['introduction'])
        assert_equals(result, ['ip_address', 'user_agent', 'participant', 'local_id'])

    def test_parts_of_day(self):
        result = self.serializer.row_for(self.stages['parts_of_day'])
        assert_equals(result, [
            'rotation_morning', 'rotation_afternoon', 'rotation_night',
            'size_morning', 'size_afternoon', 'size_night',
            'color_morning', 'color_afternoon', 'color_night'
        ])

    def test_questions_ending(self):
        result = self.serializer.row_for(self.stages['questions_ending'])
        assert_equals(result, [
            'represents_time', 'cronotype',
            'forced_size', 'forced_color', 'forced_position'
        ])

    def test_seasons_of_year(self):
        result = self.serializer.row_for(self.stages['seasons_of_year'])
        assert_equals(result, [
            'center_x_summer', 'center_x_autum', 'center_x_winter', 'center_x_spring',
            'center_y_summer', 'center_y_autum', 'center_y_winter', 'center_y_spring',
            'size_x_summer', 'size_x_autum', 'size_x_winter', 'size_x_spring',
            'size_y_summer', 'size_y_autum', 'size_y_winter', 'size_y_spring',
            'color_summer', 'color_autum', 'color_winter', 'color_spring'
        ])

    def test_timeline(self):
        result = self.serializer.row_for(self.stages['timeline'])
        assert_equals(result, [
            'line_rotation', 'line_length', 'position_my_birth', 'position_my_childhood',
            'position_my_youth', 'position_today', 'position_my_third_age', 'position_year_1900',
            'position_year_2100', 'position_wwii', 'position_the_beatles'
        ])

    def test_questions_begining(self):
        result = self.serializer.row_for(self.stages['questions_begining'])
        assert_equals(result, ['name', 'age', 'sex'])

    def test_days_of_week(self):
        result = self.serializer.row_for(self.stages['days_of_week'])
        assert_equals(result, [
            'center_x_monday', 'center_x_tuesday', 'center_x_wednesday', 'center_x_thursday', 'center_x_friday', 'center_x_saturday', 'center_x_sunday',
            'center_y_monday', 'center_y_tuesday', 'center_y_wednesday', 'center_y_thursday', 'center_y_friday', 'center_y_saturday', 'center_y_sunday',
            'size_y_monday', 'size_y_tuesday', 'size_y_wednesday', 'size_y_thursday', 'size_y_friday', 'size_y_saturday', 'size_y_sunday',
            'color_monday', 'color_tuesday', 'color_wednesday', 'color_thursday', 'color_friday', 'color_saturday', 'color_sunday'
        ])


class TestStageData:
    def setUp(self):
        self.stages = my_stages
        self.serializer = serializers.StageData()

    def test_common(self):
        result = self.serializer.common_row_for(self.stages['introduction'])
        assert_equals(result, ['a7e32988-9e4b-4a2d-bbb2-a35798e7e8f1', 1410966188680, 55448, 423])

    def test_introduction(self):
        result = self.serializer.row_for(self.stages['introduction'])
        assert_equals(result, [
            '200.0.255.1',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/37.0.2062.120 Safari/537.36',
            '324',
            'ISc_wgAqEj4ckmtm4Ir2TDw-Nfzniy0ONXF_U6kPyv1'
        ])

    def test_parts_of_day(self):
        result = self.serializer.row_for(self.stages['parts_of_day'])
        assert_equals(result, [
            167.81246306668982, 44.51096951035254, 289.75028142222305,
            76.41994897349244, 137.1224927263627, 168.7934961310493,
            'green', 'blue', 'black'
        ])

    def test_questions_ending(self):
        result = self.serializer.row_for(self.stages['questions_ending'])
        assert_equals(result, ['much', 'nocturna', 0.7, 0.3, 0.7])

    def test_seasons_of_year(self):
        result = self.serializer.row_for(self.stages['seasons_of_year'])
        assert_equals(result, [
            412.140122756362, 393.6964931190014, 386.3129272460938, 431.0544780162724,
            322.4871162027121, 207.1552720665932, 120.6320495605469, 431.5310184621541,
            488.9562232196331, 434.3308524489403, 413.3741455078125, 506.1089560325448,
            113.0257675945759, 109.6894558668137, 72.23980712890625, 110.9379630756919,
            'red', 'grey', 'blue', 'green'
        ])

    def test_timeline(self):
        result = self.serializer.row_for(self.stages['timeline'])
        assert_equals(result, [
            44.84884095673553, 724.8023584003396,
            0.9639922045259025, 0.9137393582305529, 0.5891534589279476, 0.5262852358292817,
            0.10140393087429822, 0.7737157552273286, 0.02825327829787394, 1.0, 0.9872686547323904
        ])

    def test_questions_begining(self):
        result = self.serializer.row_for(self.stages['questions_begining'])
        assert_equals(result, ['Mora', '32', 'female'])

    def test_days_of_week(self):
        result = self.serializer.row_for(self.stages['days_of_week'])
        assert_equals(result, [
            241, 123, 94, 235, 484, 356, 180,
            418.5703125, 407.1989734508097, 251.294921875, 274, 229.8177833557129, 245.1704249382019, 84.19854736328125,
            28.859375, 95.60205309838057, 155.41015625, 100, 272.3644332885742, 314.3408498764038, 146.6029052734375,
            'black', 'red', 'saddlebrown', 'blue', 'darkviolet', 'yellow', 'green'
        ])


class TestExperimentHeader:
    def setUp(self):
        self.serializer = serializers.ExperimentHeader()

    def test_complete(self):
        self.experiment = experiments.experiments_from(my_stages.values())[0]
        result = self.serializer.row_for(self.experiment)

        assert_equals(len(result), 108)
        assert_equals(result[::10], [
            'introduction_duration', 'questions_begining_sex',
            'present_past_future_radius_past',
            'seasons_of_year_center_x_spring', 'seasons_of_year_size_y_autum',
            'days_of_week_center_x_tuesday', 'days_of_week_center_y_friday', 'days_of_week_color_monday',
            'parts_of_day_rotation_afternoon',
            'timeline_line_rotation', 'timeline_position_the_beatles'
        ])

    def test_incomplete(self):
        ss = [stages.stage_from(s) for s in stages_rows[8:]]
        self.experiment = experiments.experiments_from(ss)[0]
        result = self.serializer.row_for(self.experiment)

        assert_equals(len(result), 108)
        assert_equals(result[::10], [
            'introduction_duration', 'questions_begining_sex',
            'present_past_future_radius_past',
            'seasons_of_year_center_x_spring', 'seasons_of_year_size_y_autum',
            'days_of_week_center_x_tuesday', 'days_of_week_center_y_friday', 'days_of_week_color_monday',
            'parts_of_day_rotation_afternoon',
            'timeline_line_rotation', 'timeline_position_the_beatles'
        ])


class TestExperimentData:
    def setUp(self):
        self.serializer = serializers.ExperimentData()

    def test_complete(self):
        self.experiment = experiments.experiments_from(my_stages.values())[0]
        result = self.serializer.row_for(self.experiment)
        
        assert_equals(len(result), 108)
        assert_equals(result[::10], [
            55448, 'female',
            70,
            431.0544780162724, 109.6894558668137,
            123, 229.8177833557129, 'black',
            44.51096951035254,
            44.84884095673553, 0.9872686547323904
        ])

    def test_incomplete(self):
        ss = [stages.stage_from(s) for s in stages_rows[8:]]
        self.experiment = experiments.experiments_from(ss)[0]
        result = self.serializer.row_for(self.experiment)
        
        assert_equals(len(result), 108)
        assert_equals(result[::10], [
            55448, 'female',
            70,
            431.0544780162724, 109.6894558668137,
            123, 229.8177833557129, 'black',
            44.51096951035254,
            44.84884095673553, 0.9872686547323904
        ])
