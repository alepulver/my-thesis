import serializers.stage.normal as sz_normal


def normal():
    return {
        'flat': Flat(sz_normal.FlatHeader(), sz_normal.FlatDescription(), sz_normal.FlatData()),
        'common': Common(sz_normal.FlatHeader(), sz_normal.FlatDescription(), sz_normal.FlatData()),
        'recursive_single': RecursiveSingle(sz_normal.RecursiveHeader(), sz_normal.RecursiveDescription(), sz_normal.RecursiveData()),
        'recursive_multi': RecursiveMulti(sz_normal.RecursiveHeader(), sz_normal.RecursiveDescription(), sz_normal.RecursiveData())
    }


class Flat:
    def __init__(self, header, description, data):
        self.header = header
        self.description = description
        self.data = data

    def row_header_for(self, stage_class):
        return stage_class.visit_class(self.header)

    def row_data_for(self, stage):
        return stage.visit(self.data)

    def row_description_for(self, stage_class):
        return stage_class.visit_class(self.description)


class Common:
    def __init__(self, header, description, data):
        self.header = header
        self.description = description
        self.data = data

    def row_header_for(self, stage_class):
        return self.header.common_row()

    def row_data_for(self, stage):
        return self.data.common_row_for(stage)

    def row_description_for(self, stage_class):
        return self.description.common_row()


class RecursiveSingle:
    def __init__(self, header, description, data):
        self.header = header
        self.description = description
        self.data = data

    def row_header_for(self, stage_class):
        variables = stage_class.visit_class(self.header)
        if len(variables) == 0:
            return []

        elements = stage_class.stage_elements()
        return ['{}_{}'.format(var, elem) for var in variables for elem in elements]

    def row_data_for(self, stage):
        variables = stage.visit(self.header)
        if len(variables) == 0:
            return []
        elements = type(stage).stage_elements()
        return [stage.element_data(elem)[var] for var in variables for elem in elements]

    def row_description_for(self, stage_class):
        variables = stage_class.visit_class(self.description)
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
        row = stage_class.visit_class(self.header)
        if len(row) > 0:
            row = ['element'] + row
        return row

    def rows_data_for(self, stage):
        variables = stage.visit_class(self.header)
        if len(variables) == 0:
            return []
        elements = type(stage).stage_elements()
        result = []
        for e in elements:
            values = stage.element_data(e)
            result.append([e] + [values[v] for v in variables])

        return result

    def row_description_for(self, stage_class):
        variables = stage_class.visit_class(self.description)
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
