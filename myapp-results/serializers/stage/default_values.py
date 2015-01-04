from . import empty
from serializers import groups


def create_recursive():
    obj = groups.Group(RecursiveHeader(), RecursiveDescription(), RecursiveData())
    return groups.Recursive(obj)


def create_flat():
    obj = groups.Group(FlatHeader(), FlatDescription(), FlatData())
    return groups.Flat(obj)


class RecursiveHeader(empty.StageVisitor):
    def row_for(self, stage_class):
        return stage_class.visit_class(self)

    def row(self):
        return ['default_size']

    def case_present_past_future(self, stage_class):
        return self.row()

    def case_seasons_of_year(self, stage_class):
        return self.row()

    def case_days_of_week(self, stage_class):
        return self.row()


class RecursiveDescription(empty.StageVisitor):
    def row_for(self, stage_class):
        return stage_class.visit_class(self)

    def case_present_past_future(self, stage_class):
        return ['Si el sujeto dejó intacto el radio original de 70 pixels']

    def case_seasons_of_year(self, stage_class):
        return ['Si el sujeto dejó intacto el tamaño original de 100x100 pixels']

    def case_days_of_week(self, stage_class):
        return ['Si el sujeto dejó intacto el alto original de 100 pixels']


class RecursiveData(empty.StageVisitor):
    def row_for_element(self, stage, element):
        self.data = stage.element_data(element)
        is_default = stage.visit(self)
        if is_default:
            return ['yes']
        else:
            return ['no']

    def case_present_past_future(self, stage):
        return self.data['radius'] == 70

    def case_seasons_of_year(self, stage):
        return self.data['size_x'] == 100 and self.data['size_y'] == 100

    def case_days_of_week(self, stage):
        return self.data['size_y'] == 100


class FlatHeader(empty.StageVisitor):
    def row_for(self, stage_class):
        return stage_class.visit_class(self)

    def row(self):
        return ['default_size']

    def case_present_past_future(self, stage_class):
        return self.row()

    def case_seasons_of_year(self, stage_class):
        return self.row()

    def case_days_of_week(self, stage_class):
        return self.row()


class FlatDescription(empty.StageVisitor):
    def row_for(self, stage_class):
        return stage_class.visit_class(self)

    def row(self):
        return ['Fracción de figuras con tamaño por default (0 es ninguna, 1 son todas)']

    def case_present_past_future(self, stage_class):
        return self.row()

    def case_seasons_of_year(self, stage_class):
        return self.row()

    def case_days_of_week(self, stage_class):
        return self.row()


class FlatData(empty.StageVisitor):
    def row_for(self, stage):
        self.stage = stage
        return stage.visit(self)

    def row(self):
        data_extractor = RecursiveData()
        elements = self.stage.stage_elements()
        results = [data_extractor.row_for_element(self.stage, e)[0] for e in elements]

        return [results.count('yes') / len(results)]

    def case_present_past_future(self, stage):
        return self.row()

    def case_seasons_of_year(self, stage):
        return self.row()

    def case_days_of_week(self, stage):
        return self.row()
