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

    assert_equals(len(exps), 2)
    assert_equals(len(exps[0].stages()), 0)
    assert_equals(len(exps[1].stages()), 0)
