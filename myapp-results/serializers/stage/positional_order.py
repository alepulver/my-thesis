from . import empty
import aggregators
from serializers import groups
from datetime import date


def create():
    obj = groups.Group(FlatHeader(), FlatDescription(), FlatData())
    return groups.Flat(obj)


class FlatHeader(empty.StageVisitor):
    def row_for(self, stage_class):
        return stage_class.visit_class(self)

    def case_present_past_future(self, stage_class):
        return ['order_x', 'order_y']

    def case_parts_of_day(self, stage_class):
        return ['order']

    def case_days_of_week(self, stage_class):
        return ['order_x']

    def case_timeline(self, stage_class):
        return ['order', 'order_match']


class FlatDescription(empty.StageVisitor):
    def row_for(self, stage_class):
        return stage_class.visit_class(self)

    def case_present_past_future(self, stage_class):
        return [
            'Orden de aparición en X (horizontal) de los elementos, de izquierda a derecha',
            'Orden de aparición en Y (vertical) de los elementos, de arriba a abajo'
        ]

    def case_parts_of_day(self, stage_class):
        return ['Orden en que se obican las etapas del día']

    def case_days_of_week(self, stage_class):
        return ['Orden en X (lunes primero, domingo primero u otro)']

    def case_timeline(self, stage_class):
        return [
            'Orden de la línea, según el 1900 y el 2100 (izquierda a derecha, o al revés)'
            'Similitud entre el orden correcto y el elegido, independiente de la dirección del tiempo elegida'
        ]


class FlatData(empty.StageVisitor):
    def row_for(self, stage):
        self.stage = stage
        self.order = aggregators.Order()
        return stage.visit(self)

    def get_elements_by(self, attribute):
        elements = self.stage.stage_elements()
        parts = [(p, self.stage.element_data(p)[attribute]) for p in elements]
        parts.sort(key=lambda x: x[1])
        parts = [x[0] for x in parts]
        return parts

    def case_present_past_future(self, stage):
        order_x = self.get_elements_by('center_x')
        order_y = self.get_elements_by('center_y')
        return ['_'.join(order_x), '_'.join(order_y)]

    def case_parts_of_day(self, stage):
        parts = self.get_elements_by('rotation')
        return [self.order.order_for(stage, parts)]

    def case_days_of_week(self, stage):
        parts = self.get_elements_by('center_x')
        return [self.order.order_for(stage, parts)]

    def case_timeline(self, stage):
        parts = self.get_elements_by('position')

        today = date.fromtimestamp(stage.time_start() / 1000).year
        age = int(stage.experiment.get_stage('questions_begining').age())
        ordered_parts = [
            ('year_1900', 1900),
            ('wwii', 1942),
            ('the_beatles', 1963),
            ('my_birth', today - age),
            ('my_childhood', today - age + 10),
            ('my_youth', today - age + 25),
            ('today', today),
            ('my_third_age', today - age + 60),
            ('year_2100', 2100)
        ]
        ordered_parts.sort(key=lambda x: x[1])
        ordered_parts = [x[0] for x in ordered_parts]

        line_order = self.order.order_for(stage, parts)
        order_match = self.order.matching_score(ordered_parts, parts)

        return [line_order, order_match]
