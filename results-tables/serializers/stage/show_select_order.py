import aggregators
from . import empty
from serializers import groups


def create():
    obj = groups.Group(FlatHeader(), FlatDescription(), FlatData())
    return groups.Flat(obj)


class FlatHeader(empty.StageVisitor):
    def row_for(self, stage_class):
        return stage_class.visit_class(self)

    def row(self):
        return ['show_select_match']

    def row_with_order(self):
        return self.row() + ['show_order', 'select_order']

    def case_present_past_future(self, stage_class):
        return self.row_with_order()

    def case_seasons_of_year(self, stage_class):
        return self.row_with_order()

    def case_days_of_week(self, stage_class):
        return self.row_with_order()

    def case_parts_of_day(self, stage_class):
        return self.row_with_order()

    def case_timeline(self, stage_class):
        return self.row()


class FlatDescription(empty.StageVisitor):
    def row_for(self, stage_class):
        return stage_class.visit_class(self)

    def row(self):
        return ['Medida de la similitud entre el orden en que aparecen los botones, y en que el sujeto los eligió']

    def row_with_order(self):
        return self.row() + ['Orden en que se ubicaron los botones', 'Orden en que el sujeto eligió los elementos']

    def case_present_past_future(self, stage_class):
        return self.row_with_order()

    def case_seasons_of_year(self, stage_class):
        return self.row_with_order()

    def case_days_of_week(self, stage_class):
        return self.row_with_order()

    def case_parts_of_day(self, stage_class):
        return self.row_with_order()

    def case_timeline(self, stage_class):
        return self.row()


class FlatData(empty.StageVisitor):
    def row_for(self, stage):
        return stage.visit(self)

    def row(self, stage):
        events = aggregators.Events(stage)
        return [events.order_matching()]

    def row_with_order(self, stage):
        events = aggregators.Events(stage)
        show = stage._data['results']['choose']['show_order']
        select = events.selection_order()
        score = aggregators.Order.matching_score(show, select)
        return [score, '_'.join(show), '_'.join(select)]

    def case_present_past_future(self, stage):
        return self.row_with_order(stage)

    def case_seasons_of_year(self, stage):
        return self.row_with_order(stage)

    def case_days_of_week(self, stage):
        events = aggregators.Events(stage)
        order = aggregators.Order()
        show_order = stage._data['results']['choose']['show_order']
        select_order = events.selection_order()

        return self.row(stage) + [
            order.order_for(stage, show_order),
            order.order_for(stage, select_order)
        ]

    def case_parts_of_day(self, stage):
        return self.row_with_order(stage)

    def case_timeline(self, stage):
        events = aggregators.Events(stage)

        if stage.button_order() == "chronological":
            shown = [
                'year_1900', 'wwii', 'the_beatles',
                'my_birth', 'my_childhood', 'my_youth',
                'today', 'my_third_age', 'year_2100'
            ]
        elif stage.button_order() == "unsorted":
            shown = [
                'today', 'wwii', 'my_youth',
                'my_birth', 'year_2100', 'the_beatles',
                'year_1900', 'my_childhood', 'my_third_age',
            ]

        selected = events.selection_order()
        return [aggregators.Order.matching_score(shown, selected)]
