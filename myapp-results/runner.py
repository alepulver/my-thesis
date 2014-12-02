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

    exps = experiments.experiments_from(stgs)
    print("%s total experiments" % len(exps))
    exps_complete = [e for e in exps if e.is_complete()]
    print("%s complete experiments" % len(exps_complete))

    for driverCls in serializer_drivers.all_drivers():
        driver = driverCls(args.output_dir)
        driver.serialize(exps)

    return 0


if __name__ == "__main__":
    status = main(sys.argv)
    sys.exit(status)
