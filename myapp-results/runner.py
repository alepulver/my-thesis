import os
import sys
import json
import stages
import experiments
import csv
import serializer_drivers
import argparse


def main(arguments):
    parser = argparse.ArgumentParser(description='Generate flat tables from structured results.')
    parser.add_argument(
        'input_files', metavar='FILE', type=str, nargs='+',
        help='a JSON input file to read data from'
    )
    parser.add_argument(
        '--output_dir', dest='output_dir', default='output',
        help='output directory to write the results (default: "output")'
    )

    args = parser.parse_args(arguments[1:])

    if os.path.exists(args.output_dir):
        print('ERROR: the directory "{}" already exists, please use another name'.format(args.output_dir), file=sys.stderr)
        return 1
    else:
        os.makedirs(args.output_dir)

    data_rows = []
    for file_path in args.input_files:
        with open(file_path, "r") as fp:
            data_rows.extend(json.load(fp))

    # XXX: remove old versions with incomplete data
    tedx_start_date = 1410922800000
    #other_date = 1409788800000
    condition = lambda s: ('start_time' in s.keys()) and s['start_time'] > tedx_start_date
    stgs = [stages.stage_from(r) for r in data_rows if condition(r)]
    print("%s stages" % len(stgs))

    exps = experiments.experiments_from(stgs)
    print("%s total experiments" % len(exps))

    exps_complete = [e for e in exps if e.is_complete()]
    print("%s complete experiments" % len(exps_complete))

    exps = [e for e in exps if not e.has_stage('questions_begining') or e.get_stage('questions_begining').sex() in ['male', 'female']]
    print("%s valid experiments remain" % len(exps))

    for driver in serializer_drivers.experiments_drivers():
        results = driver.serialize(exps)
        os.makedirs('{}/{}'.format(args.output_dir, driver.name))
        for name, rows in results.items():
            with open('{}/{}/{}.csv'.format(args.output_dir, driver.name, name), 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for r in rows:
                    writer.writerow(r)

    for driver in serializer_drivers.stages_drivers():
        results = driver.serialize(stgs)
        os.makedirs('{}/{}'.format(args.output_dir, driver.name))
        for name, rows in results.items():
            with open('{}/{}/{}.csv'.format(args.output_dir, driver.name, name), 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for r in rows:
                    writer.writerow(r)

    return 0


if __name__ == "__main__":
    status = main(sys.argv)
    sys.exit(status)
