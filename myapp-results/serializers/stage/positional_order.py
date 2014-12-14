from . import empty
import itertools as it


class FlatHeader(empty.StageVisitor):
    def row_for(self, stage_class):
        return stage_class.visit_class(self)

    def case_present_past_future(self, stage_class):
        return ['order_x', 'order_y']

    def case_parts_of_day(self, stage_class):
        return ['order']

    def case_days_of_week(self, stage_class):
        return ['order_x']


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


class FlatData(empty.StageVisitor):
    def row_for(self, stage):
        return stage.visit(self)

    def case_present_past_future(self, stage):
        elements = stage.stage_elements()
        data = [(e, stage.element_data(e)) for e in elements]
        
        data.sort(key = lambda x: x[1]['center_x'])
        order_x = [x[0] for x in data]

        data.sort(key = lambda x: x[1]['center_y'])
        order_y = [x[0] for x in data]

        return ['_'.join(order_x), '_'.join(order_y)]

    def case_parts_of_day(self, stage):
        parts = [(p, stage.element_data(p)['rotation']) for p in stage.stage_elements()]
        parts.sort(key = lambda x: x[1])
        parts = it.cycle(map(lambda x: x[0], parts))
        parts = it.dropwhile(lambda x: x != 'morning', parts)

        morning = next(parts)
        assert(morning == "morning")
        after_morning = next(parts)

        if after_morning == 'afternoon':
            return ['clockwise']
        else:
            return ['counterclockwise']

    def case_days_of_week(self, stage):
        parts = [(p, stage.element_data(p)['center_x']) for p in stage.stage_elements()]
        parts.sort(key = lambda x: x[1])
        parts = [x[0] for x in parts]

        monday_first = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        sunday_first = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        if parts == monday_first:
            return ['monday_first']
        elif parts == sunday_first:
            return ['sunday_first']
        else:
            return ['not_ordered']
