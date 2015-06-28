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

    def sample(self, cluster):
        items = self.clusters[cluster]
        num_items = self.num_items // len(self.clusters)
        samples = random.sample(items, num_items)
        return samples


class StratifiedSampler(Sampler):
    name = 'stratified'

    def sample(self, cluster):
        pass