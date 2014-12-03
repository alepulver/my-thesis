import serializers_stage as sz_stage
import serializers_experiment as sz_exp
import stages


def all_drivers():
    return [
        StageSummary,
        FlatStages,
        Stages,
        ExperimentSummary,
        Experiments
    ]


class CommonAggregator:
    def __init__(self, header, description, data):
        self.header = header
        self.description = description
        self.data = data

    def description(self):
        one = self.header.common_row()
        two = self.description.common_row()

        result = []
        result.append(['variable_name', 'description'])
        result.extend(zip(one, two))

        return result

    def data(self, elements):
        result = []
        result.append(self.header.common_row())
        result.extend(self.data.common_row_for(e) for e in elements)

        return result


class RecursiveAggregator:
    pass


class StageSummary:
    def serialize(self, experiments):
        stgs = []
        for exp in experiments:
            stgs.extend(exp.stages())

        results = {}

        description = []
        description.append(['variable_name', 'description'])

        header_serializer = sz_stage.FlatHeader()
        data_serializer = sz_stage.FlatDescription()
        one = ['experiment_id', 'name'] + header_serializer.common_row()
        two = ['ID única del experimento', 'Clase de etapa correspondiente a la fila'] + data_serializer.common_row()

        for r in zip(one, two):
            description.append(r)

        results['stages_description'] = description

        header_serializer = sz_stage.FlatHeader()
        data_serializer = sz_stage.FlatData()
        data = []
        data.append(['experiment_id','name'] + header_serializer.common_row())
        for s in stgs:
            data.append([s.experiment_id(), s.stage_name()] + data_serializer.common_row_for(s))
        results['stages'] = data

        return results


class FlatStages:
    def serialize(self, experiments):
        stgs = []
        for exp in experiments:
            stgs.extend(exp.stages())

        results = {}
        flat_serializer = sz_stage.FlatHeader()
        recursive_serializer = sz_stage.RecursiveHeader()
        for s in stages.all_stages():
            sn = s.stage_name()
            fn = 'stage_{}'.format(sn)
            row = ['experiment_id'] + flat_serializer.common_row() + flat_serializer.single_row_for(s) + recursive_serializer.single_row_for(s)
            results[fn] = [row]

        flat_serializer = sz_stage.FlatData()
        recursive_serializer = sz_stage.RecursiveData()
        for s in stgs:
            sn = s.stage_name()
            fn = 'stage_{}'.format(sn)
            row = flat_serializer.common_row_for(s) + flat_serializer.single_row_for(s) + recursive_serializer.single_row_for(s)
            results[fn].append([s.experiment_id()] + row)


        flat_serializer = sz_stage.FlatHeader()
        recursive_serializer = sz_stage.RecursiveHeader()
        flat_description_serializer = sz_stage.FlatDescription()
        recursive_description_serializer = sz_stage.RecursiveDescription()
        for s in stages.all_stages():
            sn = s.stage_name()
            fn = 'stage_{}_description'.format(sn)
            one = ['experiment_id'] + flat_serializer.common_row() + flat_serializer.single_row_for(s) + recursive_serializer.single_row_for(s)
            two = ['ID únco por experimento'] + flat_description_serializer.common_row() + flat_description_serializer.single_row_for(s) + recursive_description_serializer.single_row_for(s)
            row = [['variable_name', 'description']]
            row.extend(zip(one, two))
            results[fn] = row

        return results


class Stages:
    def serialize(self, experiments):
        stgs = []
        for exp in experiments:
            stgs.extend(exp.stages())

        results = {}
        header_serializer = sz_stage.RecursiveHeader()
        for s in stages.all_stages():
            sn = s.stage_name()
            fn = 'stageM_{}'.format(sn)
            row = ['experiment_id'] + header_serializer.multiple_rows_for(s)
            results[fn] = [row]

        data_serializer = sz_stage.RecursiveData()
        for s in stgs:
            sn = s.stage_name()
            fn = 'stageM_{}'.format(sn)
            for row in data_serializer.multiple_rows_for(s):
                results[fn].append([s.experiment_id()] + row)


        header_serializer = sz_stage.RecursiveHeader()
        data_serializer = sz_stage.RecursiveDescription()
        for s in stages.all_stages():
            sn = s.stage_name()
            fn = 'stageM_{}_description'.format(sn)
            one = ['experiment_id'] + header_serializer.multiple_rows_for(s)
            two = ['ID únco por experimento'] + data_serializer.multiple_rows_for(s)
            row = [['variable_name', 'description']]
            row.extend(zip(one, two))
            results[fn] = row

        return results


class ExperimentSummary:
    def serialize(self, experiments):
        results = {}

        description = []
        description.append(['variable_name', 'description'])

        header_serializer = sz_exp.SummaryHeader()
        data_serializer = sz_exp.SummaryDescription()
        one = header_serializer.row()
        two = data_serializer.row()

        for r in zip(one, two):
            description.append(r)

        results['experiments_summary_description'] = description

        header_serializer = sz_exp.SummaryHeader()
        data_serializer = sz_exp.SummaryData()
        data = []
        data.append(header_serializer.row())
        for e in experiments:
            data.append(data_serializer.row_for(e))
        results['experiments_summary'] = data

        return results


class Experiments:
    def serialize(self, experiments):
        results = {}

        description = []
        description.append(['variable_name', 'description'])

        header_serializer = sz_exp.FullHeader()
        data_serializer = sz_exp.FullDescription()
        one = header_serializer.row()
        two = data_serializer.row()

        for r in zip(one, two):
            description.append(r)

        results['experiments_description'] = description

        header_serializer = sz_exp.FullHeader()
        data_serializer = sz_exp.FullData()
        data = []
        data.append(header_serializer.row())
        for e in experiments:
            data.append(data_serializer.row_for(e))
        results['experiments'] = data

        return results
