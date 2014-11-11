import json
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


def test_stage():
    stage = stages.stage_from(rows['introduction'])

    assert_equals(stage.time_start(), 1410966188680)
    assert_equals(stage.time_duration(), 55448)
    assert_equals(stage.experiment_id(), 'a7e32988-9e4b-4a2d-bbb2-a35798e7e8f1')
    assert_equals(stage.size_in_bytes(), 423)


def test_introduction():
    stage = stages.stage_from(rows['introduction'])

    assert_equals(stage.stage_name(), 'introduction')
    assert_equals(stage.ip_address(), '200.0.255.1')
    assert_equals(stage.user_agent(), 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')
    assert_equals(stage.participant(), '324')
    assert_equals(stage.local_id(), 'ISc_wgAqEj4ckmtm4Ir2TDw-Nfzniy0ONXF_U6kPyv1')


def test_questions_begining():
    stage = stages.stage_from(rows['questions_begining'])

    assert_equals(stage.stage_name(), 'questions_begining')
    assert_equals(stage.name(), 'Mora')
    assert_equals(stage.age(), '32')
    assert_equals(stage.sex(), 'female')


def test_present_past_future():
    stage = stages.stage_from(rows['present_past_future'])
    assert_equals(stage.stage_name(), 'present_past_future')


def test_seasons_of_year():
    stage = stages.stage_from(rows['seasons_of_year'])
    assert_equals(stage.stage_name(), 'seasons_of_year')


def test_days_of_week():
    stage = stages.stage_from(rows['days_of_week'])
    assert_equals(stage.stage_name(), 'days_of_week')


def test_parts_of_day():
    stage = stages.stage_from(rows['parts_of_day'])
    assert_equals(stage.stage_name(), 'parts_of_day')


def test_timeline():
    stage = stages.stage_from(rows['timeline'])
    assert_equals(stage.stage_name(), 'timeline')


def test_questions_ending():
    stage = stages.stage_from(rows['questions_ending'])

    assert_equals(stage.stage_name(), 'questions_ending')
    assert_equals(stage.represents_time(), 'much')
    assert_equals(stage.cronotype(), 'nocturna')
    assert_equals(stage.choice_position(), 0.7)
    assert_equals(stage.choice_size(), 0.7)
    assert_equals(stage.choice_color(), 0.3)
