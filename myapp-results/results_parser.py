#!/usr/bin/env python3

import sys
import json
from collections import defaultdict
import csv


class Stage:
    def __init__(self, data, experiment):
        self._data = data
        self._experiment = experiment

    @staticmethod
    def row_header():
        return ['exp_id', 'size', 'start_time', 'end_time', 'name', 'complete']

    def size_in_bytes(self):
        return len(json.dumps(self._data))

    def row(self):
        return [
            self._data['experiment'],
            self.size_in_bytes(),
            self._data['start_time'],
            self._data['end_time'],
            self._data['stage'],
            self._experiment.is_complete()
        ]


class QuestionsBeginTedx:
    def name(self):
        return self._data['name']

    def age(self):
        return self._data['age']

    def sex(self):
        return self._data['sex']

    def working(self):
        return 'none'

    def studying(self):
        return 'none'


class QuestionsBeginExternal:
    def name(self):
        return self._data['name']

    def age(self):
        return self._data['age']

    def sex(self):
        return self._data['sex']

    def studying(self):
        return self._data['studying']

    def working(self):
        return self._data['working']


class Experiment:
    def __init__(self, data):
        self._data = data

    def get_stage(self, name):
        return next(filter(lambda s: s['stage'] == name, self._data))

    @staticmethod
    def row_header():
        return [
            'exp_id', 'size', 'num_stages', 'start_time',
            'end_time', 'participant', 'group',
            'ip_address', 'user_agent', 'local_id', 'complete'
        ]

    def size_in_bytes(self):
        return len(json.dumps(self._data))

    def end_time(self):
        end_time = max(map(lambda s: s['end_time'], self._data))
        return end_time

    def is_complete(self):
        return len(self._data) == 8

    def stages(self):
        return (Stage(s, self) for s in self._data)

    def row(self):
        introduction = self.get_stage("introduction")
        results = introduction['results']

        return [
            self._data[0]['experiment'],
            self.size_in_bytes(),
            len(self._data),
            introduction['start_time'],
            self.end_time(),
            results['participant'],
            results['group'],
            results['ip_address'],
            results['user_agent'],
            results['local_id'] if 'local_id' in results else 'unknown',
            self.is_complete()
        ]


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
