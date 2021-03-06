from . import empty
from serializers import groups


def create_flat():
    obj = groups.Group(FlatHeader(), FlatDescription(), FlatData())
    return groups.Flat(obj)


def create_recursive():
    obj = groups.Group(RecursiveHeader(), RecursiveDescription(), RecursiveData())
    return groups.Recursive(obj)


class FlatHeader(empty.StageVisitor):
    def row_for(self, stage_class):
        return stage_class.visit_class(self)

    def case_introduction(self, stage_class):
        return ['ip_address', 'user_agent', 'participant', 'local_id']

    def case_questions_begining(self, stage_class):
        return ['name', 'age', 'sex']

    def case_timeline(self, stage_class):
        return ['line_rotation', 'line_length', 'button_order']

    def case_questions_ending(self, stage_class):
        return [
            'represents_time', 'cronotype',
            'forced_size', 'forced_color',
            'forced_position', 'comments'
        ]


class FlatData(empty.StageVisitor):
    def row_for(self, stage):
        return stage.visit(self)

    def case_introduction(self, stage):
        return [stage.ip_address(), stage.user_agent(), stage.participant(), stage.local_id()]

    def case_questions_begining(self, stage):
        return [stage.name(), stage.age(), stage.sex()]

    def case_timeline(self, stage):
        return [stage.rotation(), stage.length(), stage.button_order()]

    def case_questions_ending(self, stage):
        return [
            stage.represents_time(), stage.cronotype(),
            stage.choice_size(), stage.choice_color(),
            stage.choice_position(), stage.comments()
        ]


class FlatDescription(empty.StageVisitor):
    def row_for(self, stage_class):
        return stage_class.visit_class(self)

    def case_introduction(self, stage_class):
        return [
            'Dirección IP del sujeto, permite identificar región y suele ser la misma por oficinas',
            'Navegador del sujeto, con Sistema Operativo',
            'ID de TEDx, corresponde a la tabla de cronotipos',
            'Identifica el navegador en una computadora, a ver si más de un experimento provienen de ahí'
        ]

    def case_questions_begining(self, stage_class):
        return ['Nombre', 'Edad', 'Sexo']


    def case_timeline(self, stage_class):
        return [
            'Grados de inclinación (de 0 a 360, aumenta en sentido antihorario)',
            'Longitud de la línea de tiempo',
            'Orden en que aparecen los botones (de arriba a abajo, e izuierda a derecha)'
        ]

    def case_questions_ending(self, stage_class):
        return [
            'En qué medida uno siente que representa el tiempo en el espacio',
            'Según sus hábitos el sujeto se considera una persona ...',
            'Qué tan forzado le pareció elegir el tamaño',
            'Qué tan forzado le pareció elegir el color',
            'Qué tan forzado le pareció elegir la posición',
            'Comentarios'
        ]


class RecursiveHeader(empty.StageVisitor):
    def row_for(self, stage_class):
        return stage_class.visit_class(self)

    def case_present_past_future(self, stage_class):
        return ['center_x', 'center_y', 'radius', 'color']

    def case_seasons_of_year(self, stage_class):
        return ['center_x', 'center_y', 'size_x', 'size_y', 'color']

    def case_days_of_week(self, stage_class):
        return ['center_x', 'center_y', 'size_y', 'color']

    def case_parts_of_day(self, stage_class):
        return ['rotation', 'size', 'color']

    def case_timeline(self, stage_class):
        return ['position']


class RecursiveData(empty.StageVisitor):
    def row_for_element(self, stage, element):
        self.data = stage.element_data(element)
        return stage.visit(self)

    def row(self, variables):
        return [self.data[v] for v in variables]

    def case_present_past_future(self, stage):
        return self.row(['center_x', 'center_y', 'radius', 'color'])

    def case_seasons_of_year(self, stage):
        return self.row(['center_x', 'center_y', 'size_x', 'size_y', 'color'])

    def case_days_of_week(self, stage):
        return self.row(['center_x', 'center_y', 'size_y', 'color'])

    def case_parts_of_day(self, stage):
        return self.row(['rotation', 'size', 'color'])

    def case_timeline(self, stage):
        return self.row(['position'])


class RecursiveDescription(empty.StageVisitor):
    def row_for(self, stage_class):
        return stage_class.visit_class(self)

    def case_present_past_future(self, stage):
        return [
            'Posición X (horizontal) del centro',
            'Posición Y (vertical) del centro',
            'Radio',
            'Color'
        ]

    def case_seasons_of_year(self, stage):
        return [
            'Posición X (horizontal) del centro',
            'Posición Y (vertical) del centro',
            'Tamaño en X (ancho)',
            'Tamaño en Y (alto)',
            'Color'
        ]

    def case_days_of_week(self, stage):
        return [
            'Posición X (horizontal) del centro',
            'Posición Y (vertical) del centro',
            'Tamaño en Y (alto)',
            'Color'
        ]

    def case_parts_of_day(self, stage):
        return [
            'Grados del centro (de 0 a 360, aumenta en sentido antihorario)',
            'Cuántos grados (de 0 a 360) abarca el arco',
            'Color'
        ]

    def case_timeline(self, stage):
        return [
            'Posición (de 0 a 1, comienzo y fin de la línea, respectivamente)'
        ]
