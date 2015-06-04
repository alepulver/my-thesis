import stages
import experiments
import json


class Stages:
    def __init__(self):
        stages_rows = []
        rows = {}
        my_stages = {}

        with open("examples/results.json", "r") as fp:
            stages_rows.extend(json.load(fp))

        rows['introduction'] = stages_rows[0]
        rows['parts_of_day'] = stages_rows[1]
        rows['present_past_future'] = stages_rows[2]
        rows['questions_ending'] = stages_rows[3]
        rows['seasons_of_year'] = stages_rows[4]
        rows['timeline'] = stages_rows[5]
        rows['questions_begining'] = stages_rows[6]
        rows['days_of_week'] = stages_rows[7]

        for k in rows.keys():
            my_stages[k] = stages.stage_from(rows[k])

        self._experiments = experiments.experiments_from(my_stages.values())
        self._indexed_rows = stages_rows
        self._named_rows = rows
        self._named_stages = my_stages

    def indexed_rows(self):
        return self._indexed_rows

    def named_rows(self):
        return self._named_rows

    def named_stages(self):
        return self._named_stages
