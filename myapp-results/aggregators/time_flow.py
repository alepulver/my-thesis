from toolz.dicttoolz import valmap
from vector import Vect2D


class Timeflow:
    def __init__(self, stage):
        self.stage = stage
        elements = stage.stage_elements()

        def point_for_element(e):
            data = stage.element_data(e)
            return Vect2D(data['center_x'], data['center_y'])

        element_pairs = list(zip(elements, elements[1:]+[elements[0]]))
        pair_dict = dict(zip(elements, element_pairs))
        #pair_dict = dict([(x[0], x) for x in element_pairs])
        point_dict = valmap(lambda es: (point_for_element(es[0]), point_for_element(es[1])), pair_dict)
        vector_dict = valmap(lambda ps: ps[1] - ps[0], point_dict)
        vector_pairs_dict = valmap(lambda es: (vector_dict[es[0]], vector_dict[es[1]]), pair_dict)
        self.data = {
            'angles': valmap(lambda vs: vs[0].angleBetween(vs[1]), vector_pairs_dict),
            'length': valmap(lambda v: v.length(), vector_dict)
        }

    def angle_each(self):
        return self.data['angles']

    def length_each(self):
        return self.data['length']


class PartsOfDayTimeflow:
    def __init__(self, stage):
        self.stage = stage
        elements = stage.stage_elements()

        def rotation_for_element(e):
            data = stage.element_data(e)
            return data['rotation']

        element_pairs = list(zip(elements, elements[1:]+[elements[0]]))
        pair_dict = dict(zip(elements, element_pairs))
        rotation_dict = valmap(lambda es: (rotation_for_element(es[0]), rotation_for_element(es[1])), pair_dict)
        difference_dict = valmap(lambda ps: (ps[1] - ps[0]) % 360, rotation_dict)

        self.distance = difference_dict

    def wrap_distance_each(self):
        return self.distance
