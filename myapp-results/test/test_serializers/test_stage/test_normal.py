import json
import stages
import serializers.stage_groups as sz_stage_groups
#import serializers.stage.normal as sz_normal
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
        self.serializers = sz_stage_groups.flat()
        self.rec_sz = sz_stage_groups.recursive_single()

    def common_row(self):
        return self.serializers['common'].row_header_for(None)

    def flat_row_for(self, stage):
        return self.serializers['normal'].row_header_for(stage)

    def recursive_row_for(self, stage):
        return self.rec_sz['normal'].row_header_for(stage)

    def test_common(self):
        result = self.common_row()
        assert_equals(result, ['time_start', 'time_duration', 'size_in_bytes'])

    def test_introduction(self):
        result = self.flat_row_for(stages.Introduction)
        assert_equals(result, ['ip_address', 'user_agent', 'participant', 'local_id'])

    def test_present_past_future(self):
        result = self.recursive_row_for(stages.PresentPastFuture)
        assert_equals(result, [
            'center_x_present', 'center_y_present', 'radius_present', 'color_present',
            'center_x_past', 'center_y_past', 'radius_past', 'color_past',
            'center_x_future', 'center_y_future', 'radius_future', 'color_future'
        ])

    def test_parts_of_day(self):
        result = self.recursive_row_for(stages.PartsOfDay)
        assert_equals(result, [
            'rotation_morning', 'size_morning', 'color_morning',
            'rotation_afternoon', 'size_afternoon', 'color_afternoon',
            'rotation_night', 'size_night', 'color_night'
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
            'center_x_summer', 'center_y_summer', 'size_x_summer', 'size_y_summer', 'color_summer',
            'center_x_autum', 'center_y_autum', 'size_x_autum', 'size_y_autum', 'color_autum',
            'center_x_winter', 'center_y_winter', 'size_x_winter', 'size_y_winter', 'color_winter',
            'center_x_spring', 'center_y_spring', 'size_x_spring', 'size_y_spring', 'color_spring'
        ])

    def test_timeline_flat(self):
        result = self.flat_row_for(stages.Timeline)
        assert_equals(result, [
            'line_rotation', 'line_length', 'button_order'
        ])

    def test_timeline_recursive(self):
        result = self.recursive_row_for(stages.Timeline)
        assert_equals(result, [
            'position_my_birth', 'position_my_childhood', 'position_my_youth',
            'position_today', 'position_my_third_age', 'position_year_1900',
            'position_year_2100', 'position_wwii', 'position_the_beatles'
        ])

    def test_questions_begining(self):
        result = self.flat_row_for(stages.QuestionsBegin)
        assert_equals(result, ['name', 'age', 'sex'])

    def test_days_of_week(self):
        result = self.recursive_row_for(stages.DaysOfWeek)
        assert_equals(result, [
            'center_x_monday', 'center_y_monday', 'size_y_monday', 'color_monday',
            'center_x_tuesday', 'center_y_tuesday', 'size_y_tuesday', 'color_tuesday',
            'center_x_wednesday', 'center_y_wednesday', 'size_y_wednesday', 'color_wednesday',
            'center_x_thursday', 'center_y_thursday', 'size_y_thursday', 'color_thursday',
            'center_x_friday', 'center_y_friday', 'size_y_friday', 'color_friday',
            'center_x_saturday', 'center_y_saturday', 'size_y_saturday', 'color_saturday',
            'center_x_sunday', 'center_y_sunday', 'size_y_sunday', 'color_sunday'
        ])


class TestStageData:
    def setUp(self):
        self.stages = my_stages
        self.serializers = sz_stage_groups.flat()
        self.sz_rec = sz_stage_groups.recursive_single()

    def common_row_for(self, stage):
        return self.serializers['common'].row_data_for(stage)

    def flat_row_for(self, stage):
        return self.serializers['normal'].row_data_for(stage)

    def recursive_row_for(self, stage):
        return self.sz_rec['normal'].row_data_for(stage)

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

    def test_present_past_future(self):
        result = self.recursive_row_for(self.stages['present_past_future'])
        assert_equals(result, [
            319.06804908294, 256.06804908294, 152.93195091706, 'green',
            229, 282, 70, 'blue',
            500.3393852926092, 231.6606147073908, 146.6606147073908, 'darkviolet'
        ])

    def test_parts_of_day(self):
        result = self.recursive_row_for(self.stages['parts_of_day'])
        assert_equals(result, [
            167.81246306668982, 76.41994897349244, 'green',
            44.51096951035254, 137.1224927263627, 'blue',
            289.75028142222305, 168.7934961310493, 'black'
        ])

    def test_questions_ending(self):
        result = self.flat_row_for(self.stages['questions_ending'])
        assert_equals(result, ['much', 'nocturna', 0.7, 0.3, 0.7])

    def test_seasons_of_year(self):
        result = self.recursive_row_for(self.stages['seasons_of_year'])
        assert_equals(result, [
            412.140122756362, 322.4871162027121, 488.9562232196331, 113.0257675945759, 'red',
            393.6964931190014, 207.1552720665932, 434.3308524489403, 109.6894558668137, 'grey',
            386.3129272460938, 120.6320495605469, 413.3741455078125, 72.23980712890625, 'blue',
            431.0544780162724, 431.5310184621541, 506.1089560325448, 110.9379630756919, 'green'
        ])

    def test_timeline_flat(self):
        result = self.flat_row_for(self.stages['timeline'])
        assert_equals(result, [
            44.84884095673553, 724.8023584003396, 'chronological',
        ])

    def test_timeline_recursive(self):
        result = self.recursive_row_for(self.stages['timeline'])
        assert_equals(result, [
            0.9639922045259025, 0.9137393582305529, 0.5891534589279476,
            0.5262852358292817, 0.10140393087429822, 0.7737157552273286,
            0.02825327829787394, 1.0, 0.9872686547323904
        ])

    def test_questions_begining(self):
        result = self.flat_row_for(self.stages['questions_begining'])
        assert_equals(result, ['Mora', '32', 'female'])

    def test_days_of_week(self):
        result = self.recursive_row_for(self.stages['days_of_week'])
        assert_equals(result, [
            241, 418.5703125, 28.859375, 'black',
            123, 407.1989734508097, 95.60205309838057, 'red',
            94, 251.294921875, 155.41015625, 'saddlebrown',
            235, 274, 100, 'blue',
            484, 229.8177833557129, 272.3644332885742, 'darkviolet',
            356, 245.1704249382019, 314.3408498764038, 'yellow',
            180, 84.19854736328125, 146.6029052734375, 'green'
        ])
