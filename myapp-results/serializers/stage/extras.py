class ExperimentId:
    def row_header_for(self, stage_class):
        return ['experiment_id']

    def row_data_for(self, stage):
        return [stage.experiment_id()]

    def row_description_for(self, stage_class):
        return ['ID única del experimento']


class Name:
    def row_header_for(self, stage_class):
        return ['name']

    def row_data_for(self, stage):
        return [stage.stage_name()]

    def row_description_for(self, stage_class):
        return ['Tipo de etapa correspondiente a la fila']


class Common:
    def row_header_for(self, stage_class):
        return ['time_start', 'time_duration', 'size_in_bytes']

    def row_data_for(self, stage):
        return [stage.time_start(), stage.time_duration(), stage.size_in_bytes()]

    def row_description_for(self, stage_class):
        return [
            'Fecha del inicio de la etapa, en milisegundos desde 1/1/1970',
            'Duración en milisegundos desde el inicio hasta su fin',
            'Tamaño en bytes de la etapa, aumenta cuantos más clicks y movimientos hubo'
        ]
