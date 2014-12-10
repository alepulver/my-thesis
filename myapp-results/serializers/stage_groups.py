import serializers.stage.normal as sz_normal
import serializers.stage.extras as sz_extras
import serializers.stage.default_values as sz_def_val


def flat():
    return {
        'normal': Flat(sz_normal.FlatHeader(), sz_normal.FlatDescription(), sz_normal.FlatData()),
        'common': sz_extras.Common(),
    }


def recursive_single():
    return {
        'normal': RecursiveSingle(sz_normal.RecursiveHeader(), sz_normal.RecursiveDescription(), sz_normal.RecursiveData()),
        'default_values': RecursiveSingle(sz_def_val.RecursiveHeader(), sz_def_val.RecursiveDescription(), sz_def_val.RecursiveData())
    }


def recursive_multi():
    return {
        'normal': RecursiveMulti(sz_normal.RecursiveHeader(), sz_normal.RecursiveDescription(), sz_normal.RecursiveData()),
        'default_values': RecursiveMulti(sz_def_val.RecursiveHeader(), sz_def_val.RecursiveDescription(), sz_def_val.RecursiveData())
    }


# This is to sort serializers in the same order each time, as dictionaries don't have order
def all_by_category():
    flat_sz = flat()
    rec_single_sz = recursive_single()
    rec_multi_sz = recursive_multi()
    recursive_keys = ['normal', 'default_values']

    return {
        'flat': Composite([flat_sz[k] for k in ['common', 'normal']]),
        'recursive_single': Composite([rec_single_sz[k] for k in recursive_keys]),
        'recursive_multi': Composite([rec_multi_sz[k] for k in recursive_keys])
    }


class Flat:
    def __init__(self, header, description, data):
        self.header = header
        self.description = description
        self.data = data

    def row_header_for(self, stage_class):
        return self.header.row_for(stage_class)

    def row_data_for(self, stage):
        return self.data.row_for(stage)

    def row_description_for(self, stage_class):
        return self.description.row_for(stage_class)


class RecursiveSingle:
    def __init__(self, header, description, data):
        self.header = header
        self.description = description
        self.data = data

    def row_header_for(self, stage_class):
        variables = self.header.row_for(stage_class)
        if len(variables) == 0:
            return []

        elements = stage_class.stage_elements()
        return ['{}_{}'.format(var, elem) for elem in elements for var in variables]

    def row_data_for(self, stage):
        variables = self.header.row_for(type(stage))
        if len(variables) == 0:
            return []

        elements = type(stage).stage_elements()
        result = []
        for e in elements:
            result.extend(self.data.row_for_element(stage, e))
        return result

    def row_description_for(self, stage_class):
        variables = self.description.row_for(stage_class)
        if len(variables) == 0:
            return []
        elements = stage_class.stage_elements()
        return ['{} del "{}"'.format(var, elem) for elem in elements for var in variables]


class RecursiveMulti:
    def __init__(self, header, description, data):
        self.header = header
        self.description = description
        self.data = data

    def row_header_for(self, stage_class):
        row = self.header.row_for(stage_class)
        if len(row) > 0:
            row = ['element'] + row
        return row

    def row_data_for(self, stage):
        variables = self.header.row_for(type(stage))
        if len(variables) == 0:
            return []

        elements = type(stage).stage_elements()
        result = []
        for e in elements:
            result.append([e] + self.data.row_for_element(stage, e))
        return result

    def row_description_for(self, stage_class):
        variables = self.description.row_for(stage_class)
        if len(variables) == 0:
            return []
        return ['Elemento'] + variables


class Composite:
    def __init__(self, serializers):
        self.serializers = serializers

    def row_header_for(self, stage_class):
        result = []
        for s in self.serializers:
            result.extend(s.row_header_for(stage_class))
        return result

    def row_data_for(self, stage):
        result = []
        for s in self.serializers:
            result.extend(s.row_data_for(stage))
        return result

    def row_description_for(self, stage_class):
        result = []
        for s in self.serializers:
            result.extend(s.row_description_for(stage_class))
        return result
