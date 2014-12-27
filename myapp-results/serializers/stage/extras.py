from serializers import groups


def create():
    return {
        'experiment_id': groups.Flat(ExperimentId()),
        'name': groups.Flat(Name()),
        'common': groups.Flat(Common()),
        'element': groups.Recursive(Element())
    }


class ExperimentId:
    def header_for(self, stage_class):
        return ['experiment_id']

    def data_for(self, stage):
        return [stage.experiment_id()]

    def description_for(self, stage_class):
        return ['ID única del experimento']


class Name:
    def header_for(self, stage_class):
        return ['name']

    def data_for(self, stage):
        return [stage.stage_name()]

    def description_for(self, stage_class):
        return ['Tipo de etapa correspondiente a la fila']


class Common:
    def header_for(self, stage_class):
        return ['time_start', 'time_duration', 'size_in_bytes']

    def data_for(self, stage):
        return [stage.time_start(), stage.time_duration(), stage.size_in_bytes()]

    def description_for(self, stage_class):
        return [
            'Fecha del inicio de la etapa, en milisegundos desde 1/1/1970',
            'Duración en milisegundos desde el inicio hasta su fin',
            'Tamaño en bytes de la etapa, aumenta cuantos más clicks y movimientos hubo'
        ]


class Element:
    def header_for(self, stage_class):
        return ['element']

    def data_for_element(self, stage, element):
        return [element]

    def description_for(self, stage_class):
        return ['Elemento al que corresponden las variables']
