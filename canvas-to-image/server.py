import sys
import json
import argparse
from bottle import route, run, view, abort

stages = None


def get_stages(paths):
    data_rows = []
    for file_path in paths:
        with open(file_path, "r") as fp:
            data_rows.extend(json.load(fp))

    # XXX: remove old versions with incomplete data
    tedx_start_date = 1410922800000
    discard_old = lambda s: ('start_time' in s.keys()) and s['start_time'] > tedx_start_date
    data_rows = filter(discard_old, data_rows)

    # we only keep stages including a canvas
    stages_with_canvas = ['present_past_future', 'seasons_of_year', 'days_of_week', 'parts_of_day', 'timeline']
    canvas_only = lambda s: s['stage'] in stages_with_canvas
    data_rows = filter(canvas_only, data_rows)

    return list(data_rows)


def main(arguments):
    global stages
    parser = argparse.ArgumentParser(description='Generate flat tables from structured results.')
    parser.add_argument(
        'input_files', metavar='FILE', type=str, nargs='+',
        help='a JSON input file to read data from'
    )

    args = parser.parse_args(arguments[1:])

    stages = get_stages(args.input_files)

    print("loaded %s stages" % len(stages))

    run(host='localhost', port=8080, debug=True)


@route('/stages')
@view('index_template.html')
def handle_index():
    data = []
    for s in stages:
        element = {
            'text': '{} of {}'.format(s['stage'], s['experiment']),
            'link': '/stages/{}/{}'.format(s['experiment'], s['stage'])
        }
        data.append(element)

    return {'stages': data}


@route('/stages/<experiment>/<stage>')
@view('stage_template.html')
def handle_stage(experiment, stage):
    data = filter(lambda s: s['experiment'] == experiment and s['stage'] == stage, stages)
    data = list(data)
    if len(data) > 0:
        element = data[0]
        return {
            'serialized_stage': element['results']['stage_as_json'],
            'filename': '{}.png'.format(element['experiment'])
        }
    else:
        abort(404, 'The requested stage/experiment does not exist')


if __name__ == "__main__":
    status = main(sys.argv)
    sys.exit(status)
