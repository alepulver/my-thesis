import random


def all_samplers():
    return [SimpleSampler, StratifiedSampler]


def available_names():
    return [e.name for e in all_samplers()]


def from_name(name):
    mapping = {e.name: e for e in all_samplers()}
    return mapping[name]


class Sampler:
    def __init__(self, clusters, num_items):
        self.clusters = clusters
        self.num_items = num_items

    def cluster_names(self):
        return self.clusters.keys()

    def sample(self, cluster):
        raise NotImplementedError()


class SimpleSampler(Sampler):
    name = 'simple'

    def __init__(self, clusters, num_items):
        super().__init__(clusters, num_items)
        assert(self.num_items >= len(self.clusters))

    def sample(self, cluster):
        items = self.clusters[cluster]
        num_items = self.num_items // len(self.clusters)
        samples = random.sample(items, num_items)
        return sorted(samples, key=lambda x: x['center_dist'])


class StratifiedSampler(Sampler):
    name = 'stratified'

    def __init__(self, clusters, num_items):
        super().__init__(clusters, num_items)
        assert(self.num_items >= len(self.clusters))

        total_items = sum(len(v) for v in self.clusters.values())
        self.participation = {k: (len(v) / total_items) for k, v in self.clusters.items()}

    def sample(self, cluster):
        items = self.clusters[cluster]
        num_items = round(self.num_items * self.participation[cluster])
        num_items = min(max(1, num_items), len(items))
        samples = random.sample(items, num_items)
        return sorted(samples, key=lambda x: x['center_dist'])