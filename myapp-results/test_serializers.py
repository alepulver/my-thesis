import json
import experiments
import stages
from nose.tools import assert_equals

rows = {}


def setup_module():
    with open("examples/results.json", "r") as fp:
        stages_rows = json.load(fp)

    rows['introduction'] = stages_rows[0]
    rows['parts_of_day'] = stages_rows[1]
    rows['present_past_future'] = stages_rows[2]
    rows['questions_ending'] = stages_rows[3]
    rows['seasons_of_year'] = stages_rows[4]
    rows['timeline'] = stages_rows[5]
    rows['questions_begining'] = stages_rows[6]
    rows['days_of_week'] = stages_rows[7]


def test_stageheader_common():
	pass