import json
import experiments
import stages
from nose.tools import assert_equals

rows = None
indexed_exps = {}


def setup_module():
    global rows
    with open("examples/results.json", "r") as fp:
        rows = json.load(fp)


class TestExperiments:
    @classmethod
    def setup_class(cls):
        stgs = [stages.stage_from(r) for r in rows]
        exps = experiments.experiments_from(stgs)

        cls.experiments = {}
        for e in exps:
            cls.experiments[e.experiment_id()] = e

    def test_complete(self):
        exp = self.experiments['a7e32988-9e4b-4a2d-bbb2-a35798e7e8f1']
        assert_equals(exp.has_stage('timeline'), True)
        assert_equals(type(exp.get_stage('timeline')), stages.Timeline)
        assert_equals(exp.time_start(), 1410966188680)
        assert_equals(exp.time_duration(), 556956)
        assert_equals(exp.num_stages(), 8)
        #assert_equals(exp.experiment_id(), 'a7e32988-9e4b-4a2d-bbb2-a35798e7e8f1')
        assert_equals(exp.size_in_bytes(), 131271)
        assert_equals(exp.is_complete(), True)

    def test_incomplete(self):
        exp = self.experiments['c16705a3-64c1-43e5-b70f-24a769dced32']
        assert_equals(exp.has_stage('timeline'), False)
        assert_equals(exp.num_stages(), 6)
        #assert_equals(exp.experiment_id(), 'c16705a3-64c1-43e5-b70f-24a769dced32')
        assert_equals(exp.is_complete(), False)
