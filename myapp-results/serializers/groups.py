class Flat:
    def __init__(self, serializer):
        self.serializer = serializer

    def single_header_for(self, stage_class):
        return self.serializer.header_for(stage_class)

    def single_data_for(self, stage):
        return self.serializer.data_for(stage)

    def single_description_for(self, stage_class):
        return self.serializer.description_for(stage_class)

    def multi_header_for(self, stage_class):
        return self.single_header_for(stage_class)

    def multi_data_for(self, stage):
        return [self.serializer.data_for(stage)] * len(stage.stage_elements())

    def multi_description_for(self, stage_class):
        return self.single_description_for(stage_class)


class Recursive:
    def __init__(self, serializer):
        self.serializer = serializer

    def single_header_for(self, stage_class):
        variables = self.serializer.header_for(stage_class)
        if len(variables) == 0:
            return []

        elements = stage_class.stage_elements()
        return ['{}_{}'.format(var, elem) for elem in elements for var in variables]

    def single_data_for(self, stage):
        variables = self.serializer.header_for(stage)
        if len(variables) == 0:
            return []

        elements = stage.stage_elements()
        result = []
        for e in elements:
            result.extend(self.serializer.data_for_element(stage, e))
        return result

    def single_description_for(self, stage_class):
        variables = self.serializer.description_for(stage_class)
        if len(variables) == 0:
            return []
        elements = stage_class.stage_elements()
        return ['{} del "{}"'.format(var, elem) for elem in elements for var in variables]

    def multi_header_for(self, stage_class):
        return self.serializer.header_for(stage_class)

    def multi_data_for(self, stage):
        variables = self.serializer.header_for(stage)
        if len(variables) == 0:
            return []

        elements = stage.stage_elements()
        result = []
        for e in elements:
            result.append(self.serializer.data_for_element(stage, e))
        return result

    def multi_description_for(self, stage_class):
        return self.serializer.description_for(stage_class)


class Composite:
    def __init__(self, serializers):
        self.serializers = serializers

    def single_header_for(self, stage_class):
        result = []
        for s in self.serializers:
            result.extend(s.single_header_for(stage_class))
        return result

    def single_data_for(self, stage):
        result = []
        for s in self.serializers:
            result.extend(s.single_data_for(stage))
        return result

    def single_description_for(self, stage_class):
        result = []
        for s in self.serializers:
            result.extend(s.single_description_for(stage_class))
        return result

    def multi_header_for(self, stage_class):
        result = []
        for s in self.serializers:
            result.extend(s.multi_header_for(stage_class))
        return result

    def multi_data_for(self, stage):
        if not hasattr(stage, 'stage_elements'):
            return []

        elements = stage.stage_elements()
        result = [[] for e in elements]
        for s in self.serializers:
            rows = s.multi_data_for(stage)
            if len(rows) == 0:
                continue

            for i, e in enumerate(elements):
                result[i].extend(rows[i])
        return result

    def multi_description_for(self, stage_class):
        result = []
        for s in self.serializers:
            result.extend(s.multi_description_for(stage_class))
        return result


class Group:
    def __init__(self, header, description, data):
        self.header = header
        self.description = description
        self.data = data

    def header_for(self, stage_class):
        return self.header.row_for(stage_class)

    def description_for(self, stage_class):
        return self.description.row_for(stage_class)

    def data_for(self, stage):
        return self.data.row_for(stage)

    # XXX: only one of them has this method
    def data_for_element(self, stage, element):
        return self.data.row_for_element(stage, element)


class SingleWrapper:
    def __init__(self, serializer):
        self.serializer = serializer

    def header_for(self, stage_class):
        return self.serializer.single_header_for(stage_class)

    def data_for(self, stage):
        return self.serializer.single_data_for(stage)

    def description_for(self, stage_class):
        return self.serializer.single_description_for(stage_class)


class MultiWrapper:
    def __init__(self, serializer):
        self.serializer = serializer

    def header_for(self, stage_class):
        return self.serializer.multi_header_for(stage_class)

    def data_for(self, stage):
        return self.serializer.multi_data_for(stage)

    def description_for(self, stage_class):
        return self.serializer.multi_description_for(stage_class)
