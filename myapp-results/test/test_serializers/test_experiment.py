import json
import experiments
import stages
import serializers.experiment as sz_exp
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


class TestExperimentHeader:
    def setUp(self):
        self.serializer = sz_exp.Summary()

    def test_row(self):
        result = self.serializer.row_header_for(None)

        assert_equals(len(result), 6)
        assert_equals(result, [
            'id', 'num_stages', 'start_time',
            'duration', 'is_complete', 'size_in_bytes'
        ])


class TestExperimentData:
    def setUp(self):
        self.serializer = sz_exp.Summary()

    def test_row(self):
        self.experiment = experiments.experiments_from(my_stages.values())[0]
        result = self.serializer.row_data_for(self.experiment)

        assert_equals(len(result), 6)
        assert_equals(result, [
            'a7e32988-9e4b-4a2d-bbb2-a35798e7e8f1', 8, 1410966188680,
            556956, True, 131271
        ])
