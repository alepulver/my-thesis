import sys
import json
from collections import defaultdict
import stages
import experiments
import serializers
import csv


def write_csv(header, rows, file_name):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(header)
        for r in rows:
            writer.writerow(r.row())


def main(argv):
    if len(argv) < 2:
        print('pleas provide a path to the JSON results file')
        return 1

    with open(argv[1], "r") as fp:
        stgs = json.load(fp)
    
    # XXX: remove old versions with incomplete data
    date1 = 1410922800000
    date2 = 1409788800000
    condition = lambda s: ('start_time' in s.keys()) and s['start_time'] > date1
    stgs = list(filter(condition, stgs))
    print("%s stages" % len(stgs))
    stgs = [stages.stage_from(s) for s in stgs]

    with open('stages.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header_serializer = serializers.StageHeader()
        data_serializer = serializers.StageData()

        writer.writerow(header_serializer.common_row_for(stgs[0]))
        for e in stgs:
            writer.writerow(data_serializer.common_row_for(e))

    exps = experiments.experiments_from(stgs)
    print("%s total experiments" % len(exps))
    exps = [e for e in exps if e.is_complete()]
    print("%s complete experiments" % len(exps))

    #write_csv(Experiment.row_header(), experiment_objs, 'experiments.csv')
    #write_csv(Stage.row_header(), stage_objs, 'stages.csv')

    with open('experiments.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header_serializer = serializers.ExperimentHeader()
        data_serializer = serializers.ExperimentData()

        writer.writerow(header_serializer.row_for(exps[0]))
        for e in exps:
            writer.writerow(data_serializer.row_for(e))

    return 0

if __name__ == "__main__":
    status = main(sys.argv)
    sys.exit(status)