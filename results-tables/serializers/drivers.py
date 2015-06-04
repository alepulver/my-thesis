import serializers.stage_groups as sz_stage
import serializers.experiment as sz_exp
import serializers.stage.extras as sz_stage_extras
from serializers import groups
import stages


def stages_drivers():
    all_serializers = sz_stage.all_by_category()
    flat = sz_stage.flat()
    extras = sz_stage_extras.create()

    classes = {}
    for s in stages.all_stages():
        classes[s.stage_name()] = s

    summary_sz = groups.Composite([
        extras['experiment_id'], extras['name'], flat['common']
    ])
    flat_sz = groups.Composite([
        extras['experiment_id'], all_serializers['flat'], all_serializers['recursive']
    ])
    recursive_sz = groups.Composite([
        extras['experiment_id'], extras['element'], all_serializers['recursive']
    ])

    return [
        Summary(groups.SingleWrapper(summary_sz), 'stages_summary'),
        FlatByClass(groups.SingleWrapper(flat_sz), classes),
        MultipleRowsByClass(groups.MultiWrapper(recursive_sz), classes)
    ]


def experiments_drivers():
    return [
        Summary(sz_exp.Full(), 'experiments_full'),
        Summary(sz_exp.Summary(), 'experiments_summary')
    ]


class Summary:
    def __init__(self, serializer, name):
        self.name = name
        self.serializer = serializer

    def serialize(self, things):
        results = {}

        description = []
        description.append(['variable_name', 'description'])
        one = self.serializer.header_for(None)
        two = self.serializer.description_for(None)
        for r in zip(one, two):
            description.append(r)
        results['description'] = description

        data = []
        data.append(self.serializer.header_for(None))
        for x in things:
            data.append(self.serializer.data_for(x))
        results['data'] = data

        return results


class FlatByClass:
    def __init__(self, serializer, classes):
        self.serializer = serializer
        self.classes = classes
        self.name = "individual_stages"

    def serialize(self, things):
        results = {}

        for sn, s in self.classes.items():
            fn = sn
            row = self.serializer.header_for(s)
            results[fn] = [row]

        for s in things:
            sn = s.stage_name()
            fn = sn
            row = self.serializer.data_for(s)
            results[fn].append(row)

        for sn, s in self.classes.items():
            fn = '{}_description'.format(sn)
            one = self.serializer.header_for(s)
            two = self.serializer.description_for(s)
            row = [['variable_name', 'description']]
            row.extend(zip(one, two))
            results[fn] = row

        return results


class MultipleRowsByClass:
    def __init__(self, serializer, classes):
        self.serializer = serializer
        self.classes = classes
        self.name = "individual_stages_long"

    def serialize(self, things):
        results = {}

        for sn, s in self.classes.items():
            fn = sn
            row = self.serializer.header_for(s)
            results[fn] = [row]

        for s in things:
            sn = s.stage_name()
            fn = sn
            for row in self.serializer.data_for(s):
                results[fn].append(row)

        for sn, s in self.classes.items():
            fn = '{}_description'.format(sn)
            one = self.serializer.header_for(s)
            two = self.serializer.description_for(s)
            row = [['variable_name', 'description']]
            row.extend(zip(one, two))
            results[fn] = row

        return results
