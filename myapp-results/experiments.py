from collections import defaultdict


def experiments_from(stages):
    experiments = defaultdict(list)
    for s in stages:
        experiments[s.experiment_id()].append(s)

    return [Experiment(exp_stages) for exp_stages in experiments.values()]


class Experiment:
    def __init__(self, data):
        assert(len(data) <= 8)
        self._data = data

    def has_stage(self, stage):
        return len(list(filter(lambda s: s.stage_name() == stage.stage_name(), self._data))) > 0

    def stage_named(self, name):
        return next(filter(lambda s: s.stage_name() == name, self._data))

    def time_start(self):
        pass

    def time_duration(self):
        pass

    def num_stages(self):
        pass

    def experiment_id(self):
        return self._data[0].experiment_id()

    def size_in_bytes(self):
        return len(json.dumps(self._data))

    def end_time(self):
        end_time = max(map(lambda s: s['end_time'], self._data))
        return end_time

    def is_complete(self):
        return len(self._data) == 8

    def stages(self):
        return self._data
