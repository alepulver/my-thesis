import json
import results_parser as rp


def stages_rows():
    with open("examples/results.json", "r") as fp:
        stages = json.load(fp)

    return stages


def test_blah():
    stage = rp.Stage(stages_rows()[0], None)
