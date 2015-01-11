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
            'relatedness', 'dominance',
            'relatedness_ext', 'dominance_ext',
            'coverage'
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
            'Medida "relatedness" total de Cottle',
            'Medida "dominance" total de Cottle',
            'Medida "relatedness" total extendida',
            'Medida "dominance" total extendida',
            "Medida de cobertura total del canvas (en porcentaje)"
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
        calcCottle = aggregators.Cottle(self.stage)
        calcExt = aggregators.ExtendedCottle(self.stage)

        return [
            calcCottle.relatedness_all(),
            calcCottle.dominance_all(),
            calcExt.relatedness_all(),
            calcExt.dominance_all(),
            calcExt.coverage_all()
        ]

    def case_present_past_future(self, stage):
        return self.row()

    def case_seasons_of_year(self, stage):
        return self.row()

    def case_parts_of_day(self, stage):
        calcCottle = aggregators.PartsOfDayCottle(self.stage)
        calcExt = aggregators.PartsOfDayExtendedCottle(self.stage)

        return [
            calcCottle.relatedness_all(),
            calcCottle.dominance_all(),
            calcExt.relatedness_all(),
            calcExt.dominance_all(),
            calcExt.coverage_all()
        ]

    def case_days_of_week(self, stage):
        return self.row()


class RecursiveHeader(empty.StageVisitor):
    def row_for(self, stage_class):
        return stage_class.visit_class(self)

    def row(self):
        return [
            'relatedness', 'dominance',
            'relatedness_ext', 'dominance_ext',
            'coverage'
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
            'Medida "relatedness" específica de Cottle',
            'Medida "dominance" específica de Cottle',
            'Medida "relatedness" específica extendida',
            'Medida "dominance" específica extendida',
            "Medida de cobertura específica del canvas (en porcentaje)"
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
        self.element = element
        return stage.visit(self)

    def row(self, stage):
        if self.stage != stage:
            self.calcCottle = aggregators.Cottle(stage)
            self.calcExt = aggregators.ExtendedCottle(stage)
            #self.calcPod = aggregators.PartsOfDayCottle(stage)
            self.stage = stage

        return [
            self.calcCottle.relatedness_each()[self.element],
            self.calcCottle.dominance_each()[self.element],
            self.calcExt.relatedness_each()[self.element],
            self.calcExt.dominance_each()[self.element],
            self.calcExt.coverage_each()[self.element]
        ]

    def case_present_past_future(self, stage):
        return self.row(stage)

    def case_seasons_of_year(self, stage):
        return self.row(stage)

    def case_parts_of_day(self, stage):
        calcCottle = aggregators.PartsOfDayCottle(stage)
        calcExt = aggregators.PartsOfDayExtendedCottle(stage)

        return [
            calcCottle.relatedness_each()[self.element],
            calcCottle.dominance_each()[self.element],
            calcExt.relatedness_each()[self.element],
            calcExt.dominance_each()[self.element],
            calcExt.coverage_each()[self.element]
        ]

    def case_days_of_week(self, stage):
        return self.row(stage)
