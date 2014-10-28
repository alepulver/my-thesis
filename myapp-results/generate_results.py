import codecs
import requests
from collections import defaultdict
import json as js
import sys

def get_color(color_string):
    return unicode([u'black', u'yellow', u'saddlebrown', u'darkviolet', u'grey', u'red', u'green', u'blue'].index(color_string))

def get_declared_cronotipe(cronotipo_string):
    return unicode([u'muy_matutina',u'matutina',u'neutral',u'nocturna', u'muy_nocturna'].index(cronotipo_string))

def get_sex(sex_string):
    return unicode([u'male', u'female', u'other'].index(sex_string))

def get_time_representation(time_string):
    return unicode([u'much', u'little', u'nothing'].index(time_string))

def get_index_of_stage(time_string):
    return [u'introduction', u'questions_begining', u'present_past_future', u'seasons_of_year', u'days_of_week', u'parts_of_day', u'timeline', u'questions_ending'].index(time_string)

def get_yes_no(yn_string):
    return unicode([u'yes', u'no'].index(yn_string))


def print_questions_header(csv):
    # csv.write(u'questions_name\tquestion_age\tquestion_sex\tquestion_study\tquestion_work\t')
    csv.write(u'question_age\tquestion_sex\tquestion_study\tquestion_work\t')


def print_present_past_future_header(csv):
    csv.write(u'future_x\tfuture_y\tfuture_color\tfuture_radius\t')
    csv.write(u'past_x\tpast_y\tpast_color\tpast_radius\t')
    csv.write(u'present_x\tpresent_y\tpresent_color\tpresent_radius\t')


def print_seasons_of_year_header(csv):
    csv.write(u'summer_x\tsummer_y\tsummer_color\tsummer_width\tsummer_height\t')
    csv.write(u'spring_x\tspring_y\tspring_color\tspring_width\tspring_height\t')
    csv.write(u'winter_x\twinter_y\twinter_color\twinter_width\twinter_height\t')
    csv.write(u'autum_x\tautum_y\tautum_color\tautum_width\tautum_height\t')


def print_parts_of_day_header(csv):
    csv.write(u'morning_rotation\tmorning_angle\tmorning_color\t')
    csv.write(u'night_rotation\tnight_angle\tnight_color\t')
    csv.write(u'afternoon_rotation\tafternoon_angle\tafternoon_color\t')


def print_days_of_week_header(csv):
    csv.write(u'friday_x\tfriday_y\tfriday_width\tfriday_height\tfriday_color\t')
    csv.write(u'monday_x\tmonday_y\tmonday_width\tmonday_height\tmonday_color\t')
    csv.write(u'thursday_x\tthursday_y\tthursday_width\tthursday_height\tthursday_color\t')
    csv.write(u'sunday_x\tsunday_y\tsunday_width\tsunday_height\tsunday_color\t')
    csv.write(u'wednesday_x\twednesday_y\twednesday_width\twednesday_height\twednesday_color\t')
    csv.write(u'tuesday_x\ttuesday_y\ttuesday_width\ttuesday_height\ttuesday_color\t')
    csv.write(u'saturday_x\tsaturday_y\tsaturday_width\tsaturday_height\tsaturday_color\t')


def print_timeline_header(csv):
    csv.write(u'timeline_length\ttimeline_rotation\t')
    csv.write(u'timeline_my_birth_pos\ttimeline_my_childhood_pos\t')
    csv.write(u'timeline_my_youth_pos\ttimeline_today_pos\ttimeline_my_third_age_pos\t')
    csv.write(u'timeline_year_1900_pos\ttimeline_year_2100_pos\ttimeline_wwii_pos\t')
    csv.write(u'timeline_the_beatles_pos\t')


def print_questions_ending_header(csv):
    csv.write(u'questions_ending_represents_time\tquestions_ending_daynight\tquestions_ending_slider_size\tquestions_ending_slider_color\tquestions_ending_slider_position')


def print_questions(question_stage,csv, experimento_result):
    stage = question_stage[u'stage']
    if(stage == u'questions_begining'):
        res = unicode(question_stage[u'results'][u'age']) + u'\t'
        res = res + get_sex(question_stage[u'results'][u'sex']) + u'\t'
        # res = res +  unicode(question_stage[u'results'][u'sex']) + u'\t'
        res = res + get_yes_no(unicode(question_stage[u'results'][u'studying'])) + u'\t'
        res = res +  get_yes_no(unicode(question_stage[u'results'][u'working'])) + u'\t'
        experimento_result[u'questions_begining'] = res


def print_timeline(question_stage,csv, experimento_result):
    stage = question_stage[u'stage']
    if(stage == u'timeline'):
        res = unicode(question_stage[u'results'][u'timeline'][u'results'][u'length']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'timeline'][u'results'][u'rotation']) + u'\t'

        try:
            res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'my_birth'][u'position']) + u'\t'
        except Exception, e:
            res = res + unicode(u'\t')

        try:
            res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'my_childhood'][u'position']) + u'\t'

        except Exception, e:
            res = res + unicode(u'\t')

        try:
            res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'my_youth'][u'position']) + u'\t'

        except Exception, e:
            res = res + unicode(u'\t')

        try:
            res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'today'][u'position']) + u'\t'
        except Exception, e:
            res = res + unicode(u'\t')

        try:
            res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'my_third_age'][u'position']) + u'\t'
        except Exception, e:
            res = res + unicode(u'\t')

        try:
            res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'year_1900'][u'position']) + u'\t'
        except Exception, e:
            res = res + unicode(u'\t')

        try:
            res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'year_2100'][u'position']) + u'\t'
        except Exception, e:
            res = res + unicode(u'\t')

        try:
            res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'wwii'][u'position']) + u'\t'
        except Exception, e:
            res = res + unicode(u'\t')

        try:
            res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'the_beatles'][u'position']) + u'\t'
        except Exception, e:
            res = res + unicode(u'\t')
        experimento_result[u'timeline'] = res

def print_parts_of_day(question_stage,csv, experimento_result):
    stage = question_stage[u'stage']
    if(stage == u'parts_of_day'):
        res = unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'morning'][u'rotation']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'morning'][u'angle']) + u'\t'
        res = res + get_color(unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'morning'][u'color'])) + u'\t'

        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'night'][u'rotation']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'night'][u'angle']) + u'\t'
        res = res + get_color(unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'night'][u'color'])) + u'\t'

        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'afternoon'][u'rotation']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'afternoon'][u'angle']) + u'\t'
        res = res + get_color(unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'afternoon'][u'color'])) + u'\t'
        experimento_result[u'parts_of_day'] = res


def print_days_of_week(question_stage,csv, experimento_result):
    stage = question_stage[u'stage']
    if(stage == u'days_of_week'):
        res = unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'friday'][u'position'][u'x']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'friday'][u'position'][u'y']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'friday'][u'size'][u'width']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'friday'][u'size'][u'height']) + u'\t'
        res = res + get_color(unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'friday'][u'color'])) + u'\t'

        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'monday'][u'position'][u'x']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'monday'][u'position'][u'y']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'monday'][u'size'][u'width']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'monday'][u'size'][u'height']) + u'\t'
        res = res + get_color(unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'monday'][u'color'])) + u'\t'

        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'thursday'][u'position'][u'x']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'thursday'][u'position'][u'y']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'thursday'][u'size'][u'width']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'thursday'][u'size'][u'height']) + u'\t'
        res = res + get_color(unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'thursday'][u'color'])) + u'\t'

        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'sunday'][u'position'][u'x']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'sunday'][u'position'][u'y']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'sunday'][u'size'][u'width']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'sunday'][u'size'][u'height']) + u'\t'
        res = res + get_color(unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'sunday'][u'color'])) + u'\t'

        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'wednesday'][u'position'][u'x']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'wednesday'][u'position'][u'y']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'wednesday'][u'size'][u'width']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'wednesday'][u'size'][u'height']) + u'\t'
        res = res + get_color(unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'wednesday'][u'color'])) + u'\t'

        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'tuesday'][u'position'][u'x']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'tuesday'][u'position'][u'y']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'tuesday'][u'size'][u'width']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'tuesday'][u'size'][u'height']) + u'\t'
        res = res + get_color(unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'tuesday'][u'color'])) + u'\t'

        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'saturday'][u'position'][u'x']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'saturday'][u'position'][u'y']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'saturday'][u'size'][u'width']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'saturday'][u'size'][u'height']) + u'\t'
        res = res + get_color(unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'saturday'][u'color'])) + u'\t'
        experimento_result[u'days_of_week'] = res


def print_present_past_future(question_stage,csv, experimento_result):
    stage = question_stage[u'stage']
    if(stage == u'present_past_future'):
        res = unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'future'][u'position'][u'x']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'future'][u'position'][u'y']) + u'\t'
        res = res + get_color(unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'future'][u'color'])) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'future'][u'radius']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'past'][u'position'][u'x']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'past'][u'position'][u'y']) + u'\t'
        res = res + get_color(unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'past'][u'color'])) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'past'][u'radius']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'present'][u'position'][u'x']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'present'][u'position'][u'y']) + u'\t'
        res = res + get_color(unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'present'][u'color'])) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'present'][u'radius']) + u'\t'
        experimento_result[u'present_past_future'] = res


def print_seasons_of_year(question_stage,csv, experimento_result):
    stage = question_stage[u'stage']
    if(stage == u'seasons_of_year'):
        res = unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'summer'][u'position'][u'x']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'summer'][u'position'][u'y']) + u'\t'
        res = res + get_color(unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'summer'][u'color'])) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'summer'][u'size'][u'width']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'summer'][u'size'][u'height']) + u'\t'

        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'spring'][u'position'][u'x']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'spring'][u'position'][u'y']) + u'\t'
        res = res + get_color(unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'spring'][u'color'])) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'spring'][u'size'][u'width']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'spring'][u'size'][u'height']) + u'\t'

        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'winter'][u'position'][u'x']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'winter'][u'position'][u'y']) + u'\t'
        res = res + get_color(unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'winter'][u'color'])) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'winter'][u'size'][u'width']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'winter'][u'size'][u'height']) + u'\t'

        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'autum'][u'position'][u'x']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'autum'][u'position'][u'y']) + u'\t'
        res = res + get_color(unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'autum'][u'color'])) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'autum'][u'size'][u'width']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'drawing'][u'shapes'][u'autum'][u'size'][u'height']) + u'\t'
        experimento_result[u'seasons_of_year'] = res


def print_questions_ending(question_stage, csv, experimento_result):
    stage = question_stage[u'stage']
    if(stage == u'questions_ending'):
        res = get_time_representation(unicode(question_stage[u'results'][u'represents_time'])) + u'\t'
        res = res + get_declared_cronotipe(unicode(question_stage[u'results'][u'daynight'])) + u'\t'
        res = res + unicode(question_stage[u'results'][u'slider-size']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'slider-color']) + u'\t'
        res = res + unicode(question_stage[u'results'][u'slider-position'])
        experimento_result[u'questions_ending'] = res


def main():
    # link = "http://circles-experiment.meteor.com/results_json"
    # link = "file:///home/chudi/trabajo/neuro/neuro-circles-json-to-csv/2014-09-108-results_json.json"


    # f = requests.get(link)

    bad_experiments = [u'e7bef789-7572-4d6d-9b08-3c08143e7cde',
                       u'e2d1a338-1059d-4db3-b7f5-0804ddca0a1c',
                       u'98a6eba7-4090-44c1-b879-8c6e1f0be2e4',
                       u'5fcccc6a-85c8-4a7e-a0ca-9db05ee78856',
                       u'e7bef789-7572-4d6d-9b08-3c08143e7cde',
                       u'19455c91-8e5d-49d6-b805-3abad90cdf2b',
                       u'89d1b397-0e73-41d2-96d3-694f2c17e36d',
                       u'97e56cc9-0ddf-4331-a46e-c1ea26a73e3b',
                       u'27468044-edde-4c8a-9cc9-cdf8d57ba009',
                       u'6c1e9a03-b1a3-4daa-86de-917e6597c9fc',
                       u'093a4d6c-4c12-4aa2-b911-5f2492a14e64',
                       u'6000d89f-cd88-435b-88ac-cf5f85943e1e',
                       u'093a4d6c-4c12-4aa2-b911-5f2492a14e64',
                       u'e17362ed-c452-4890-b7de-04c4c4585ae6',
                       u'beae299f-1073f-46d4-9ab6-72a281b9302c']
    # json = f.json()
    # json_data = open('2014-09-108-results_json.json')
    json = js.loads(open(sys.argv[1]).read().decode('utf-8'))


    bad_experiments_file = open('incompletos.json', 'w')

    # json = js.load(json_data)
    with codecs.open('circles.csv', 'w', encoding='utf-8') as csv:
        users_stages = {}
        users_stages = defaultdict(list)

        for x in json:
            if x[u'start_time'] > 1410922800000:
                users_stages[x[u'experiment']].append(x)

        print_questions_header(csv)

        print_present_past_future_header(csv)

        print_seasons_of_year_header(csv)

        print_parts_of_day_header(csv)

        print_days_of_week_header(csv)

        print_timeline_header(csv)

        print_questions_ending_header(csv)

        csv.write('\n')

        print "#experimentos: " + str(len(users_stages))
        experimentos_incompleto = 0
        experimentos_completo = 0
        experimentos_con_pozos = 0
        for experimento in users_stages:
            if experimento in bad_experiments:
                continue
            experimento_result = {}
            experimento_completo = True
            # print "#cant de stages x experimento: " + str(len(users_stages[experimento]))
            # print "experimento: " + str(experimento)
            for q_stage in users_stages[experimento]:
                try:
                    print_questions(q_stage, csv, experimento_result)
                    print_present_past_future(q_stage, csv, experimento_result)
                    print_seasons_of_year(q_stage, csv, experimento_result)
                    print_parts_of_day(q_stage, csv, experimento_result)
                    print_days_of_week(q_stage, csv, experimento_result)
                    print_timeline(q_stage, csv, experimento_result)
                    print_questions_ending(q_stage, csv, experimento_result)
                except Exception:
                    pass

            if experimento_result:
                try:
                    csv.write(experimento_result[u'questions_begining'])
                except Exception:
                    experimento_completo = False
                    csv.write('-10\t-10\t-10\t-10\t')

                try:
                    csv.write(experimento_result[u'present_past_future'])
                except Exception:
                    experimento_completo = False
                    csv.write('-10\t-10\t-10\t-10\t')
                    csv.write('-10\t-10\t-10\t-10\t')
                    csv.write('-10\t-10\t-10\t-10\t')
                try:
                    csv.write(experimento_result[u'seasons_of_year'])
                except Exception:
                    experimento_completo = False
                    csv.write('-10\t-10\t-10\t-10\t')
                    csv.write('-10\t-10\t-10\t-10\t')
                    csv.write('-10\t-10\t-10\t-10\t')
                    csv.write('-10\t-10\t-10\t-10\t')
                    csv.write('-10\t-10\t-10\t-10\t')
                try:
                    csv.write(experimento_result[u'parts_of_day'])
                except Exception:
                    experimento_completo = False
                    csv.write('-10\t-10\t-10\t-10\t')
                    csv.write('-10\t-10\t-10\t-10\t')
                    csv.write('-10\t')

                try:
                    csv.write(experimento_result[u'days_of_week'])
                except Exception:
                    experimento_completo = False
                    csv.write('-10\t-10\t-10\t-10\t')
                    csv.write('-10\t-10\t-10\t-10\t')
                    csv.write('-10\t-10\t-10\t-10\t')
                    csv.write('-10\t-10\t-10\t-10\t')
                    csv.write('-10\t-10\t-10\t-10\t')
                    csv.write('-10\t-10\t-10\t-10\t')
                    csv.write('-10\t-10\t-10\t-10\t')
                    csv.write('-10\t-10\t-10\t-10\t')
                    csv.write('-10\t-10\t-10\t')

                try:
                    csv.write(experimento_result[u'timeline'])
                except Exception:
                    experimento_completo = False
                    csv.write('-10\t-10\t-10\t-10\t')
                    csv.write('-10\t-10\t-10\t-10\t')
                    csv.write('-10\t-10\t-10\t')

                try:
                    csv.write(experimento_result[u'questions_ending'])
                except Exception:
                    experimento_completo = False
                    csv.write('-10\t-10\t-10\t-10\t')
                    csv.write('-10')

                csv.write('\n')

            if not experimento_completo:
                experimentos_incompleto += 1
                bad_experiments_file.write(experimento + '\n')
                lista = []
                for stage in users_stages[experimento]:
                    bad_experiments_file.write(js.dumps(stage[u'stage']) + '\n')
                    lista.append(get_index_of_stage(stage[u'stage']))

                lista.sort()
                for i in range(len(lista) - 1):
                    if lista[i + 1] - lista[i] > 1:
                        print "hay un hueco"

            else:
                experimentos_completo += 1

        print "#experimentos incompletos: " + str(experimentos_incompleto)
        print "#experimentos completos: " + str(experimentos_completo)

if __name__ == "__main__":
    main()
