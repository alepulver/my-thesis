from . import empty
from serializers import groups
import aggregators


def create_recursive():
    obj = groups.Group(RecursiveHeader(), RecursiveDescription(), RecursiveData())
    return groups.Recursive(obj)


class RecursiveHeader(empty.StageVisitor):
    def row_for(self, stage_class):
        return stage_class.visit_class(self)

    def row(self):
        return [
            'timeflow_angle', 'timeflow_length', 'timeflow_vector_angle'
        ]

    def case_present_past_future(self, stage_class):
        return self.row()

    def case_seasons_of_year(self, stage_class):
        return self.row()

    def case_days_of_week(self, stage_class):
        return self.row()

    def case_parts_of_day(self, stage_class):
        return [
            'timeflow_arc'
        ]


class RecursiveDescription(empty.StageVisitor):
    def row_for(self, stage_class):
        return stage_class.visit_class(self)

    def row(self):
        return [
            'Ángulo entre el elemento y el siguiente (cronológico)',
            'Distancia entre el elemento y el siguiente (cronológico)',
            'Ángulo entre el vector anterior y siguiente al elemento (cronológico)'
        ]

    def case_present_past_future(self, stage_class):
        return self.row()

    def case_seasons_of_year(self, stage_class):
        return self.row()

    def case_days_of_week(self, stage_class):
        return self.row()

    def case_parts_of_day(self, stage_class):
        return [
            'Grados entre el elemento y el siguiente (cronológico)'
        ]


class RecursiveData(empty.StageVisitor):
    def __init__(self):
        self.stage = None

    def row_for_element(self, stage, element):
        self.element = element
        return stage.visit(self)

    def row(self, stage):
        if self.stage != stage:
            self.timeflow = aggregators.Timeflow(stage)

        return [
            self.timeflow.angle_each()[self.element],
            self.timeflow.length_each()[self.element],
            self.timeflow.vector_angle_each()[self.element]
        ]

    def case_present_past_future(self, stage):
        return self.row(stage)

    def case_seasons_of_year(self, stage):
        return self.row(stage)

    def case_days_of_week(self, stage):
        return self.row(stage)

    def case_parts_of_day(self, stage):
        timeflow_pod = aggregators.PartsOfDayTimeflow(stage)

        return [
            timeflow_pod.wrap_distance_each()[self.element]
        ]
