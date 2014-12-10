from . import stage_groups as sz_stage
import stages


class Summary:
    def row_header_for(self, experiment_class):
        return [
            'id', 'num_stages', 'start_time',
            'duration', 'is_complete', 'size_in_bytes'
        ]

    def row_data_for(self, experiment):
        return [
            experiment.experiment_id(), experiment.num_stages(), experiment.time_start(),
            experiment.time_duration(), experiment.is_complete(), experiment.size_in_bytes()
        ]

    def row_description_for(self, experiment_class):
        return [
            'Identificador único del experimento',
            'Cantidad de etapas del experimento (en total son 8)',
            'Fecha del inicio del experimento, en milisegundos desde 1/1/1970',
            'Duración en milisegundos desde el inicio hasta su fin',
            'Verdadero si están todas las etapas, y falso si falta alguna',
            'Tamaño en bytes del experimento, aumenta cuantos más clicks y movimientos hubo'
        ]


class Full:
    def __init__(self):
        serializers = sz_stage.normal()
        self.summary = Summary()
        self.serializer = sz_stage.Composite([serializers['common'], serializers['flat'], serializers['recursive_single']])

    def row_header_for(self, experiment_class):
        result = []
        result.extend(self.summary.row_header_for(experiment_class))
        for stage in stages.all_stages():
            sn = stage.stage_name()
            fields = self.serializer.row_header_for(stage)
            fields = ["{}_{}".format(sn, f) for f in fields]
            result.extend(fields)
        return result

    def row_data_for(self, experiment):
        result = []
        result.extend(self.summary.row_data_for(experiment))
        for stage in stages.all_stages():
            sn = stage.stage_name()
            if experiment.has_stage(sn):
                current = experiment.get_stage(sn)
                fields = self.serializer.row_data_for(current)
            else:
                headers = self.serializer.row_header_for(stage)
                fields = ['missing'] * len(headers)
            result.extend(fields)
        return result

    def row_description_for(self, experiment_class):
        result = []
        result.extend(self.summary.row_description_for(experiment_class))
        for stage in stages.all_stages():
            sn = stage.stage_name()
            fields = self.serializer.row_description_for(stage)
            fields = ['{} para la etapa "{}"'.format(f, sn) for f in fields]
            result.extend(fields)
        return result
