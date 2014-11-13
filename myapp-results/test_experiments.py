import json
import experiments
import stages
from nose.tools import assert_equals

rows = None


def setup_module():
    global rows
    with open("examples/results.json", "r") as fp:
        rows = json.load(fp)


def test_experiments():
    stgs = [stages.stage_from(r) for r in rows]
    exps = experiments.experiments_from(stgs)
    indexed_exps = {}
    for e in exps:
        indexed_exps[e.experiment_id()] = e

    assert_equals(len(exps), 2)
    assert_equals(len(indexed_exps['c16705a3-64c1-43e5-b70f-24a769dced32'].stages()), 6)
    assert_equals(indexed_exps['c16705a3-64c1-43e5-b70f-24a769dced32'].is_complete(), False)

    assert_equals(len(indexed_exps['a7e32988-9e4b-4a2d-bbb2-a35798e7e8f1'].stages()), 8)
    assert_equals(indexed_exps['a7e32988-9e4b-4a2d-bbb2-a35798e7e8f1'].is_complete(), True)
