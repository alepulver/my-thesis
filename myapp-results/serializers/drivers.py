import serializers.stage_groups as sz_stage
import serializers.experiment as sz_exp
import serializers.stage.extras as sz_stage_extras
import stages


def stages_drivers():
    normal = sz_stage.normal()
    classes = {}
    for s in stages.all_stages():
        classes[s.stage_name()] = s

    summary_sz = sz_stage.Composite([
        sz_stage_extras.ExperimentId(), sz_stage_extras.Name(), normal['common']
    ])
    flat_sz = sz_stage.Composite([
        sz_stage_extras.ExperimentId(), normal['common'],
        normal['flat'], normal['recursive_single']
    ])

    return [
        Summary(summary_sz, 'stages_summary'),
        FlatByClass(flat_sz, classes),
        MultipleRowsByClass(normal['recursive_multi'], classes)
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
        one = self.serializer.row_header_for(None)
        two = self.serializer.row_description_for(None)
        for r in zip(one, two):
            description.append(r)
        results['description'] = description

        data = []
        data.append(self.serializer.row_header_for(None))
        for x in things:
            data.append(self.serializer.row_data_for(x))
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
            row = self.serializer.row_header_for(s)
            results[fn] = [row]

        for s in things:
            sn = s.stage_name()
            fn = sn
            row = self.serializer.row_data_for(s)
            results[fn].append(row)

        for sn, s in self.classes.items():
            fn = '{}_description'.format(sn)
            one = self.serializer.row_header_for(s)
            two = self.serializer.row_description_for(s)
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
            row = self.serializer.row_header_for(s)
            results[fn] = [row]

        for s in things:
            sn = s.stage_name()
            fn = sn
            for row in self.serializer.rows_data_for(s):
                results[fn].append(row)

        for sn, s in self.classes.items():
            fn = '{}_description'.format(sn)
            one = self.serializer.row_header_for(s)
            two = self.serializer.row_description_for(s)
            row = [['variable_name', 'description']]
            row.extend(zip(one, two))
            results[fn] = row

        return results
