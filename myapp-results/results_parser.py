#!/usr/bin/env python3

import sys
import json
from collections import defaultdict
import csv


def write_csv(header, rows, file_name):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(header)
        for r in rows:
            writer.writerow(r.row())


def main(argv):
    with open(argv[1], "r") as fp:
        stages = json.load(fp)
    # XXX: remove old versions with incomplete data
    condition = lambda s: ('start_time' in s.keys()) and s['start_time'] > 1409788800000
    stages = list(filter(condition, stages))
    print("%s stages" % len(stages))

    experiments = defaultdict(list)
    for s in stages:
        experiments[s['experiment']].append(s)
    print("%s experiments" % len(experiments))

    experiment_objs = [Experiment(e) for e in experiments.values()]
    stage_objs = [s for e in experiment_objs for s in e.stages()]

    write_csv(Experiment.row_header(), experiment_objs, 'experiments.csv')
    write_csv(Stage.row_header(), stage_objs, 'stages.csv')

    return 0


if __name__ == "__main__":
    status = main(sys.argv)
    sys.exit(status)
