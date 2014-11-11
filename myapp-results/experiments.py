from collections import defaultdict


def experiments_from(stages):
    experiments = defaultdict(list)
    for s in stages:
        experiments[s.experiment_id()].append(s)

    return [Experiment(exp_stages) for exp_stages in experiments.values()]


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

