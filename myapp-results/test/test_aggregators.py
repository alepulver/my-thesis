import json
import stages
import aggregators
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


def test_xxx():
    x = aggregators.Events(my_stages['present_past_future'])
    r = x.color_changes()
    assert_equals(r, {'past': 1, 'future': 1, 'present': 3})


def test_yyy():
    x = aggregators.Events(my_stages['parts_of_day'])
    assert_equals(x.order_matching(), -1)
    x = aggregators.Events(my_stages['present_past_future'])
    assert_equals(x.order_matching(), -1/3)
