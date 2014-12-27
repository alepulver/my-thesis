from collections import defaultdict
import stages


def experiments_from(stages):
    experiments = defaultdict(list)
    for s in stages:
        experiments[s.experiment_id()].append(s)

    return [Experiment(exp_stages) for exp_stages in experiments.values()]


class Experiment:
    def __init__(self, stage_list):
        assert(len(stage_list) > 0)

        self._data = {}
        for s in stage_list:
            self._data[s.stage_name()] = s
            s.experiment = self

        assert(len(stage_list) == len(self._data))

    def has_stage(self, name):
        return name in self._data.keys()

    def get_stage(self, name):
        return self._data[name]

    def stages(self):
        return self._data.values()

    def time_start(self):
        return self._data['introduction'].time_start()

    def time_duration(self):
        return sum(s.time_duration() for s in self._data.values())

    def num_stages(self):
        return len(self._data)

    def experiment_id(self):
        return self._data['introduction'].experiment_id()

    def size_in_bytes(self):
        return sum(s.size_in_bytes() for s in self._data.values())

    def is_complete(self):
        return len(self._data) == len(stages.all_stages())
