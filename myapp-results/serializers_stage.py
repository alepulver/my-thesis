class FlatHeader:
    def single_row_for(self, stage):
        return stage.visit_header(self)

    def multiple_rows_for(self, stage):
        raise NotImplementedError()

    def common_row(self):
        return ['time_start', 'time_duration', 'size_in_bytes']

    def case_introduction(self, stage):
        return ['ip_address', 'user_agent', 'participant', 'local_id']

    def case_questions_begining(self, stage):
        return ['name', 'age', 'sex']

    def case_present_past_future(self, stage):
        return []

    def case_seasons_of_year(self, stage):
        return []

    def case_days_of_week(self, stage):
        return []

    def case_parts_of_day(self, stage):
        return []

    def case_timeline(self, stage):
        return ['line_rotation', 'line_length']

    def case_questions_ending(self, stage):
        return ['represents_time', 'cronotype', 'forced_size', 'forced_color', 'forced_position']


class RecursiveHeader:
    def single_row_for(self, stage):
        if len(stage.visit_header(self)) == 0:
            return []
        variables = stage.visit_header(self)
        elements = stage.stage_elements()
        return ['{}_{}'.format(var, elem) for var in variables for elem in elements]

    def multiple_rows_for(self, stage):
        row = stage.visit_header(self)
        if len(row) > 0:
            row = ['element'] + row
        return row

    def common_row(self):
        return []

    def case_introduction(self, stage):
        return []

    def case_questions_begining(self, stage):
        return []

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

    def case_questions_ending(self, stage):
        return []


class FlatData:
    def single_row_for(self, stage):
        return stage.visit(self)

    def multiple_rows_for(self, stage):
        raise NotImplementedError()

    def common_row_for(self, stage):
        return [stage.time_start(), stage.time_duration(), stage.size_in_bytes()]

    def case_introduction(self, stage):
        return [stage.ip_address(), stage.user_agent(), stage.participant(), stage.local_id()]

    def case_questions_begining(self, stage):
        return [stage.name(), stage.age(), stage.sex()]

    def case_present_past_future(self, stage):
        return []

    def case_seasons_of_year(self, stage):
        return []

    def case_days_of_week(self, stage):
        return []

    def case_parts_of_day(self, stage):
        return []

    def case_timeline(self, stage):
        return [stage.rotation(), stage.length()]

    def case_questions_ending(self, stage):
        return [
            stage.represents_time(), stage.cronotype(),
            stage.choice_size(), stage.choice_color(), stage.choice_position()
        ]


class RecursiveData:
    def single_row_for(self, stage):
        if len(stage.visit_header(self)) == 0:
            return []
        variables = stage.visit_header(self)
        elements = type(stage).stage_elements()
        return [stage.element_data(elem)[var] for var in variables for elem in elements]

    def multiple_rows_for(self, stage):
        variables = stage.visit_header(self)
        if len(variables) == 0:
            return []
        elements = type(stage).stage_elements()
        result = []
        for e in elements:
            values = stage.element_data(e)
            result.append([e] + [values[v] for v in variables])

        return result

    def common_row_for(self, stage):
        return []

    def case_introduction(self, stage):
        return []

    def case_questions_begining(self, stage):
        return []

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

    def case_questions_ending(self, stage):
        return []


class FlatDescription:
    def single_row_for(self, stage):
        return stage.visit_header(self)

    def multiple_rows_for(self, stage):
        raise NotImplementedError()

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

    def case_present_past_future(self, stage):
        return []

    def case_seasons_of_year(self, stage):
        return []

    def case_days_of_week(self, stage):
        return []

    def case_parts_of_day(self, stage):
        return []

    def case_timeline(self, stage):
        return [
            'Grados de inclinación (de -90 a 90) de la línea, negativo hacia arriba y positivo hacia abajo',
            'Longitud de la línea de tiempo'
        ]

    def case_questions_ending(self, stage):
        return [
            'En qué medida uno siente que representa el tiempo en el espacio',
            'Según sus hábitos el sujeto se considera una persona ...',
            'Qué tan forzado le pareció elegir el tamaño',
            'Qué tan forzado le pareció elegir el color',
            'Qué tan forzado le pareció elegir la posición'
        ]


class RecursiveDescription:
    def single_row_for(self, stage):
        if len(stage.visit_header(self)) == 0:
            return []
        variables = stage.visit_header(self)
        elements = stage.stage_elements()
        return ['{} del "{}"'.format(var, elem) for var in variables for elem in elements]

    def multiple_rows_for(self, stage):
        variables = stage.visit_header(self)
        if len(variables) == 0:
            return []
        return ['Elemento'] + variables

    def common_row(self):
        return []

    def case_introduction(self, stage):
        return []

    def case_questions_begining(self, stage):
        return []

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

    def case_questions_ending(self, stage):
        return []
