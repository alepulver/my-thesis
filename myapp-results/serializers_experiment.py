import serializers_stage as sz_stage
import stages


class SummaryHeader:
    def row(self):
        return [
            'id', 'num_stages', 'start_time',
            'duration', 'is_complete', 'size_in_bytes'
        ]


class FullHeader:
    def row(self):
        serializer = [sz_stage.FlatHeader(), sz_stage.RecursiveHeader()]
        result = []
        for stage in stages.all_stages():
            sn = stage.stage_name()
            fields = serializer[0].common_row() + serializer[0].single_row_for(stage) + serializer[1].single_row_for(stage)
            fields = ["{}_{}".format(sn, f) for f in fields]
            result.extend(fields)
        return result


class SummaryData:
    def row_for(self, experiment):
        return [
            experiment.experiment_id(), experiment.num_stages(), experiment.time_start(),
            experiment.time_duration(), experiment.is_complete(), experiment.size_in_bytes()
        ]


class FullData:
    def row_for(self, experiment):
        serializer = [sz_stage.FlatData(), sz_stage.RecursiveData()]
        result = []
        for stage in stages.all_stages():
            sn = stage.stage_name()
            if experiment.has_stage(sn):
                current = experiment.get_stage(sn)
                fields = serializer[0].common_row_for(current) + serializer[0].single_row_for(current) + serializer[1].single_row_for(current)
            else:
                one = sz_stage.FlatHeader().common_row()
                two = sz_stage.FlatHeader().single_row_for(stage)
                three = sz_stage.RecursiveHeader().single_row_for(stage)
                fields = ['missing'] * (len(one) + len(two) + len(three))
            result.extend(fields)
        return result


class SummaryDescription:
    def row(self):
        return [
            'Identificador único del experimento',
            'Cantidad de etapas del experimento (en total son 8)',
            'Fecha del inicio de la etapa, en milisegundos desde 1/1/1970',
            'Duración en milisegundos desde el inicio hasta su fin',
            'Verdadero si están todas las etapas, y falso si falta alguna',
            'Tamaño en bytes de la etapa, aumenta cuantos más clicks y movimientos hubo'
        ]


class FullDescription:
    def row(self):
        serializer = [sz_stage.FlatDescription(), sz_stage.RecursiveDescription()]
        result = []
        for stage in stages.all_stages():
            sn = stage.stage_name()
            fields = serializer[0].common_row() + serializer[0].single_row_for(stage) + serializer[1].single_row_for(stage)
            fields = ['{} para la etapa "{}"'.format(f, sn) for f in fields]
            result.extend(fields)
        return result
