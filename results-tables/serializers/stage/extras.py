from serializers import groups
from datetime import datetime


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
        return ['time_start', 'time_duration', 'hour']

    def data_for(self, stage):
        hour = datetime.fromtimestamp(stage.time_start() / 1000).hour
        return [stage.time_start(), stage.time_duration(), hour]

    def description_for(self, stage_class):
        return [
            'Fecha del inicio de la etapa, en milisegundos desde 1/1/1970',
            'Duración en milisegundos desde el inicio hasta su fin',
            'Hora del día (según el navegador, en su zona horaria) del inicio de la etapa'
        ]


class Element:
    def header_for(self, stage_class):
        return ['element']

    def data_for_element(self, stage, element):
        return [element]

    def description_for(self, stage_class):
        return ['Elemento al que corresponden las variables']
