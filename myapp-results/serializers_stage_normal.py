import serializers_stage_empty as empty


class FlatHeader(empty.FlatHeader):
    def common_row(self):
        return ['time_start', 'time_duration', 'size_in_bytes']

    def case_introduction(self, stage):
        return ['ip_address', 'user_agent', 'participant', 'local_id']

    def case_questions_begining(self, stage):
        return ['name', 'age', 'sex']

    def case_timeline(self, stage):
        return ['line_rotation', 'line_length', 'button_order']

    def case_questions_ending(self, stage):
        return ['represents_time', 'cronotype', 'forced_size', 'forced_color', 'forced_position']


class RecursiveHeader(empty.RecursiveHeader):
    def case_present_past_future(self, stage):
        return ['center_x', 'center_y', 'radius', 'color']

    def case_seasons_of_year(self, stage):
        return ['center_x', 'center_y', 'size_x', 'size_y', 'color']

    def case_days_of_week(self, stage):
        return ['center_x', 'center_y', 'size_y', 'color']

    def case_parts_of_day(self, stage):
        return ['rotation', 'size', 'color']

    def case_timeline(self, stage):
        return ['position']


class FlatData(empty.FlatData):
    def common_row_for(self, stage):
        return [stage.time_start(), stage.time_duration(), stage.size_in_bytes()]

    def case_introduction(self, stage):
        return [stage.ip_address(), stage.user_agent(), stage.participant(), stage.local_id()]

    def case_questions_begining(self, stage):
        return [stage.name(), stage.age(), stage.sex()]

    def case_timeline(self, stage):
        return [stage.rotation(), stage.length(), stage.button_order()]

    def case_questions_ending(self, stage):
        return [
            stage.represents_time(), stage.cronotype(),
            stage.choice_size(), stage.choice_color(), stage.choice_position()
        ]


class RecursiveData(empty.RecursiveData):
    def case_present_past_future(self, stage):
        return ['center_x', 'center_y', 'radius', 'color']

    def case_seasons_of_year(self, stage):
        return ['center_x', 'center_y', 'size_x', 'size_y', 'color']

    def case_days_of_week(self, stage):
        return ['center_x', 'center_y', 'size_y', 'color']

    def case_parts_of_day(self, stage):
        return ['rotation', 'size', 'color']

    def case_timeline(self, stage):
        return ['position']


class FlatDescription(empty.FlatDescription):
    def common_row(self):
        return [
            'ID único por experimento',
            'Fecha del inicio de la etapa, en milisegundos desde 1/1/1970',
            'Duración en milisegundos desde el inicio hasta su fin',
            'Tamaño en bytes de la etapa, aumenta cuantos más clicks y movimientos hubo'
        ]

    def case_introduction(self, stage):
        return [
            'Dirección IP del sujeto, permite identificar región y suele ser la misma por oficinas',
            'Navegador del sujeto, con Sistema Operativo',
            'ID de TEDx, corresponde a la tabla de cronotipos',
            'Identifica el navegador en una computadora, a ver si más de un experimento provienen de ahí'
        ]

    def case_questions_begining(self, stage):
        return ['Nombre', 'Edad', 'Sexo']

    def case_timeline(self, stage):
        return [
            'Grados de inclinación (de -90 a 90) de la línea, negativo hacia arriba y positivo hacia abajo',
            'Longitud de la línea de tiempo',
            'Orden en que aparecen los botones (de arriba a abajo, e izuierda a derecha)'
        ]

    def case_questions_ending(self, stage):
        return [
            'En qué medida uno siente que representa el tiempo en el espacio',
            'Según sus hábitos el sujeto se considera una persona ...',
            'Qué tan forzado le pareció elegir el tamaño',
            'Qué tan forzado le pareció elegir el color',
            'Qué tan forzado le pareció elegir la posición'
        ]


class RecursiveDescription(empty.RecursiveDescription):
    def case_present_past_future(self, stage):
        return [
            'Posición X (vertical) del centro',
            'Posición Y (vertical) del centro',
            'Radio',
            'Color'
        ]

    def case_seasons_of_year(self, stage):
        return [
            'Posición X (vertical) del centro',
            'Posición Y (vertical) del centro',
            'Tamaño en X (ancho)',
            'Tamaño en Y (alto)',
            'Color'
        ]

    def case_days_of_week(self, stage):
        return [
            'Posición X (vertical) del centro',
            'Posición Y (vertical) del centro',
            'Tamaño en Y (alto)',
            'Color'
        ]

    def case_parts_of_day(self, stage):
        return [
            'Grados del cenro (de 0 a 360, aumenta en sentido horario)',
            'Cuántos grados (de 0 a 360) abarca el arco',
            'Color'
        ]

    def case_timeline(self, stage):
        return [
            'Posición (de 0 a 1, comienzo y fin de la línea, respectivamente)'
        ]
