from . import empty
from serializers import groups
import aggregators


def create_flat():
    obj = groups.Group(FlatHeader(), FlatDescription(), FlatData())
    return groups.Flat(obj)


def create_recursive():
    obj = groups.Group(RecursiveHeader(), RecursiveDescription(), RecursiveData())
    return groups.Recursive(obj)


class FlatHeader(empty.StageVisitor):
    def row_for(self, stage_class):
        return stage_class.visit_class(self)

    def row(self):
        return [
            'relatedness_cottle', 'dominance_cottle',
            'relatedness_group', 'dominance_group'
        ]

    def case_present_past_future(self, stage_class):
        return self.row()

    def case_seasons_of_year(self, stage_class):
        return self.row()

    def case_parts_of_day(self, stage_class):
        return self.row()

    def case_days_of_week(self, stage_class):
        return self.row()


class FlatDescription(empty.StageVisitor):
    def row_for(self, stage_class):
        return stage_class.visit_class(self)

    def row(self):
        return [
            'Medida "relatedness" de Cottle (por etapa)',
            'Medida "dominance" de Cottle (por etapa)',
            'Grupo para "relatedness" de Cottle (por etapa)',
            'Grupo para "dominance" de Cottle (por etapa)'
        ]

    def case_present_past_future(self, stage_class):
        return self.row()

    def case_seasons_of_year(self, stage_class):
        return self.row()

    def case_parts_of_day(self, stage_class):
        return self.row()

    def days_of_week(self, stage_class):
        return self.row()


class FlatData(empty.StageVisitor):
    def row_for(self, stage):
        self.stage = stage
        return stage.visit(self)

    def row(self):
        calculator = aggregators.CottleWrapper(self.stage)

        return calculator.row_for_stage()

    def case_present_past_future(self, stage):
        return self.row()

    def case_seasons_of_year(self, stage):
        return self.row()

    def case_parts_of_day(self, stage):
        return self.row()

    def case_days_of_week(self, stage):
        return self.row()


class RecursiveHeader(empty.StageVisitor):
    def row_for(self, stage_class):
        return stage_class.visit_class(self)

    def row(self):
        return [
            'relatedness_cottle', 'dominance_cottle'
        ]

    def case_present_past_future(self, stage_class):
        return self.row()

    def case_seasons_of_year(self, stage_class):
        return self.row()

    def case_parts_of_day(self, stage_class):
        return self.row()

    def case_days_of_week(self, stage_class):
        return self.row()


class RecursiveDescription(empty.StageVisitor):
    def row_for(self, stage_class):
        return stage_class.visit_class(self)

    def row(self):
        return [
            'Medida "relatedness" de Cottle (por elemento)',
            'Medida "dominance" de Cottle (por elemento)'
        ]

    def case_present_past_future(self, stage_class):
        return self.row()

    def case_seasons_of_year(self, stage_class):
        return self.row()

    def case_parts_of_day(self, stage_class):
        return self.row()

    def case_days_of_week(self, stage_class):
        return self.row()


class RecursiveData(empty.StageVisitor):
    def __init__(self):
        self.stage = None

    def row_for_element(self, stage, element):
        if self.stage != stage:
            self.calculator = aggregators.CottleWrapper(stage)
            self.stage = stage

        self.element = element
        return stage.visit(self)

    def row(self):
        return self.calculator.row_for_element(self.element)

    def case_present_past_future(self, stage):
        return self.row()

    def case_seasons_of_year(self, stage):
        return self.row()

    def case_parts_of_day(self, stage):
        return self.row()

    def case_days_of_week(self, stage):
        return self.row()
