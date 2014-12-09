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
