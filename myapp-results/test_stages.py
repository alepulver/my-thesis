import json
import stages
from nose.tools import assert_equals
import copy

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
    assert_equals(stage.element_data('present'), {
        'center_x': 319.06804908294, 'center_y': 256.06804908294,
        'color': 'green', 'radius': 152.93195091706
    })
    assert_equals(stage.element_data('past'), {
        'center_x': 229, 'center_y': 282, 'color': 'blue', 'radius': 70
    })
    assert_equals(stage.element_data('future'), {
        'center_x': 500.3393852926092, 'center_y': 231.6606147073908,
        'color': 'darkviolet', 'radius': 146.6606147073908
    })


def test_seasons_of_year():
    stage = stages.stage_from(rows['seasons_of_year'])
    
    assert_equals(stage.stage_name(), 'seasons_of_year')
    assert_equals(stage.element_data('winter'), {
        'center_x': 386.3129272460938, 'center_y': 120.6320495605469,
        'color': 'blue',
        'size_x': 413.3741455078125, 'size_y': 72.23980712890625
    })
    assert_equals(stage.element_data('summer'), {
        'center_x': 412.140122756362, 'center_y': 322.4871162027121,
        'color': 'red',
        'size_x': 488.9562232196331, 'size_y': 113.0257675945759
    })
    assert_equals(stage.element_data('spring'), {
        'center_x': 431.0544780162724, 'center_y': 431.5310184621541,
        'color': 'green',
        'size_x': 506.1089560325448, 'size_y': 110.9379630756919
    })
    assert_equals(stage.element_data('autum'), {
        'center_x': 393.6964931190014, 'center_y': 207.1552720665932,
        'color': 'grey',
        'size_x': 434.3308524489403, 'size_y': 109.6894558668137
    })


def test_days_of_week():
    stage = stages.stage_from(rows['days_of_week'])
    assert_equals(stage.stage_name(), 'days_of_week')


def test_parts_of_day():
    stage = stages.stage_from(rows['parts_of_day'])

    assert_equals(stage.stage_name(), 'parts_of_day')
    assert_equals(stage.element_data('morning'), {
        'color': 'green',
        'size': 76.41994897349244,
        'rotation': 167.81246306668982
    })
    assert_equals(stage.element_data('afternoon'), {
        'color': 'blue',
        'size': 137.1224927263627,
        'rotation': 44.51096951035254
    })
    assert_equals(stage.element_data('night'), {
        'color': 'black',
        'size': 168.7934961310493,
        'rotation': 289.75028142222305
    })


def test_parts_of_day_angles_should_wraparound():
    my_row = copy.deepcopy(rows['parts_of_day'])
    shapes = my_row['results']['drawing']['shapes']
    shapes['morning']['rotation'] = 370
    shapes['morning']['angle'] = -10
    shapes['night']['rotation'] = 730
    shapes['night']['angle'] = -370
    stage = stages.stage_from(my_row)

    assert_equals(stage.element_data('morning'), {
        'color': 'green', 'size': 350, 'rotation': 185
    })
    assert_equals(stage.element_data('night'), {
        'color': 'black', 'size': 350, 'rotation': 185
    })


def test_timeline():
    stage = stages.stage_from(rows['timeline'])

    assert_equals(stage.stage_name(), 'timeline')
    assert_equals(stage.length(), 724.8023584003396)
    assert_equals(stage.rotation(), 44.84884095673553)
    assert_equals(stage.button_order(), 'chronological')
    assert_equals(stage.element_data('year_1900'), {
        'position': 0.7737157552273286
    })
    assert_equals(stage.element_data('the_beatles'), {
        'position': 0.9872686547323904
    })
    assert_equals(stage.element_data('wwii'), {
        'position': 1
    })
    assert_equals(stage.element_data('year_2100'), {
        'position': 0.02825327829787394
    })
    assert_equals(stage.element_data('my_third_age'), {
        'position': 0.10140393087429822
    })
    assert_equals(stage.element_data('my_birth'), {
        'position': 0.9639922045259025
    })
    assert_equals(stage.element_data('my_childhood'), {
        'position': 0.9137393582305529
    })
    assert_equals(stage.element_data('my_youth'), {
        'position': 0.5891534589279476
    })
    assert_equals(stage.element_data('today'), {
        'position': 0.5262852358292817
    })


def test_questions_ending():
    stage = stages.stage_from(rows['questions_ending'])

    assert_equals(stage.stage_name(), 'questions_ending')
    assert_equals(stage.represents_time(), 'much')
    assert_equals(stage.cronotype(), 'nocturna')
    assert_equals(stage.choice_position(), 0.7)
    assert_equals(stage.choice_size(), 0.7)
    assert_equals(stage.choice_color(), 0.3)
