from . import empty
import aggregators


class RecursiveHeader(empty.StageVisitor):
    def row_for(self, stage_class):
        return stage_class.visit_class(self)

    def row(self):
        return ['total_events', 'time_spent', 'num_selects', 'num_moves', 'num_resizes', 'num_color_changes']

    def case_present_past_future(self, stage_class):
        return self.row()

    def case_seasons_of_year(self, stage_class):
        return self.row()

    def case_days_of_week(self, stage_class):
        return self.row()

    def case_parts_of_day(self, stage_class):
        return self.row()

    def case_timeline(self, stage_class):
        return ['total_events', 'time_spent', 'num_selects', 'num_moves']


class RecursiveDescription(empty.StageVisitor):
    def row_for(self, stage_class):
        return stage_class.visit_class(self)

    def row(self):
        return [
            'Cantidad total de eventos',
            'Tiempo en milisegundos transcurridos con la figura seleccionada',
            'Cantidad de selecciones',
            'Cantidad de movimientos',
            'Cantidad de redimensiones',
            'Cantidad de cambios de color'
        ]

    def case_present_past_future(self, stage_class):
        return self.row()

    def case_seasons_of_year(self, stage_class):
        return self.row()

    def case_days_of_week(self, stage_class):
        return self.row()

    def case_parts_of_day(self, stage_class):
        return self.row()

    def case_timeline(self, stage_class):
        return [
            'Cantidad total de eventos',
            'Tiempo en milisegundos transcurridos con la figura seleccionada',
            'Cantidad de selecciones',
            'Cantidad de movimientos',
        ]

class RecursiveData(empty.StageVisitor):
    def __init__(self):
        self.stage = None
        self.event_types = ['select', 'drag', 'resize', 'color']

    def row_for_element(self, stage, element):
        if self.stage != stage:
            self.stage = stage
            self.data = self.calculate()

        self.element = element
        return stage.visit(self)

    def calculate(self):
        events = aggregators.Events(self.stage)
        results = {}
        for et in self.event_types:
            results[et] = events.count_by_type(et)

        results['time'] = events.time_spent()
        return results

    def row(self):
        event_data = [self.data[et][self.element] for et in self.event_types]
        total = sum(event_data)
        return [total, self.data['time'][self.element]] + event_data

    def case_present_past_future(self, stage):
        return self.row()

    def case_seasons_of_year(self, stage):
        return self.row()

    def case_days_of_week(self, stage):
        return self.row()

    def case_parts_of_day(self, stage):
        return self.row()

    def case_timeline(self, stage):
        event_data = [self.data[et][self.element] for et in ['select', 'drag']]
        total = sum(event_data)
        return [total, self.data['time'][self.element]] + event_data
