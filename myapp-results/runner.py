import sys
import json
import stages
import experiments
import serializers
import csv
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

    # FIXME: create output dir if doesn't exist, fail if does

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

    output_common_stages(args.output_dir, stgs)

    exps = experiments.experiments_from(stgs)
    print("%s total experiments" % len(exps))
    exps_complete = [e for e in exps if e.is_complete()]
    print("%s complete experiments" % len(exps_complete))

    output_experiments(args.output_dir, exps)

    output_individual_stages(args.output_dir, stgs)

    return 0


def output_common_stages(output_dir, stgs):
    with open('{}/stages.csv'.format(output_dir), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header_serializer = serializers.StageHeader()
        data_serializer = serializers.StageData()

        writer.writerow(header_serializer.common_row())
        for e in stgs:
            writer.writerow(data_serializer.common_row_for(e))


def output_experiments(output_dir, exps):
    with open('{}/experiments.csv'.format(output_dir), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header_serializer = serializers.ExperimentHeader()
        data_serializer = serializers.ExperimentData()

        writer.writerow(header_serializer.row())
        for e in exps:
            writer.writerow(data_serializer.row_for(e))


def output_individual_stages(output_dir, stgs):
    writers = {}
    a_serializer = serializers.StageHeader()
    for s in stages.all_stages():
        sn = s.stage_name()
        csv_file = open('{}/stage_{}.csv'.format(output_dir, sn), 'w', newline='')
        csv_writer = csv.writer(csv_file)
        writers[sn] = csv_writer

        csv_writer.writerow(a_serializer.common_row() + a_serializer.row_for(s))

    a_serializer = serializers.StageData()
    for s in stgs:
        sn = s.stage_name()
        writers[sn].writerow(a_serializer.common_row_for(s) + a_serializer.row_for(s))


if __name__ == "__main__":
    status = main(sys.argv)
    sys.exit(status)
