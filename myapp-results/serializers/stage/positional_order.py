from . import empty


class FlatHeader(empty.StageVisitor):
    def case_present_past_future(self, stage_class):
        return ['order_x', 'order_y']


class FlatDescription(empty.StageVisitor):
    def case_present_past_future(self, stage_class):
        return [
            'Órden de aparición en X (horizontal) de los elementos, de izquierda a derecha',
            'Órden de aparición en Y (vertical) de los elementos, de arriba a abajo'
        ]


class FlatData(empty.StageVisitor):
    def case_present_past_future(self, stage):
        elements = stage.stage_elements()
        pass

