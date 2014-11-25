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

        assert(len(stage_list) == len(self._data))

    def has_stage(self, stage):
        return stage.stage_name() in self._data.keys()

    def stage_named(self, name):
        return self._data[name]

    def time_start(self):
        pass

    def time_duration(self):
        pass

    def num_stages(self):
        pass

    def experiment_id(self):
        return self._data['introduction'].experiment_id()

    def size_in_bytes(self):
        return sum(s.size_in_bytes() for s in self._data.values())

    def end_time(self):
        end_time = max(map(lambda s: s['end_time'], self._data))
        return end_time

    def is_complete(self):
        return len(self._data) == len(stages.all_stages())

    def stages(self):
        return self._data
