import serializer_drivers
from nose.tools import assert_equals

# FIXME: move CSV writing code out of serializer drivers, and return dictionary of rows for each file

class TestExperimentHeader:
    def setUp(self):
        self.serializer = serializers.ExperimentHeader()

    def test_row(self):
        result = self.serializer.row()

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
            4113, 'male', 70, 687, 100, 209, 142,
            'black', 145.0, 'missing', 'missing'
        ])
