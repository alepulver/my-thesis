import serializers.stage.normal as sz_normal
import serializers.stage.extras as sz_extras


def normal():
    return {
        'flat': Flat(sz_normal.FlatHeader(), sz_normal.FlatDescription(), sz_normal.FlatData()),
        'common': sz_extras.Common(),
        'recursive_single': RecursiveSingle(sz_normal.RecursiveHeader(), sz_normal.RecursiveDescription(), sz_normal.RecursiveData()),
        'recursive_multi': RecursiveMulti(sz_normal.RecursiveHeader(), sz_normal.RecursiveDescription(), sz_normal.RecursiveData())
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
        return ['{}_{}'.format(var, elem) for var in variables for elem in elements]

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
        return ['{} del "{}"'.format(var, elem) for var in variables for elem in elements]


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

    def rows_data_for(self, stage):
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
