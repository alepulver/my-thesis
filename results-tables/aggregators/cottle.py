from shapely.geometry import Point, box, Polygon
from toolz.dicttoolz import valmap
from functools import reduce
import math


class CottleWrapper:
    def __init__(self, stage):
        self.cottle = Cottle(stage)

    def row_for_stage(self):
        return [
            self.cottle.relatedness_all(),
            self.cottle.dominance_all(),
            self.cottle.relatedness_group(),
            self.cottle.dominance_group(),
        ]

    def row_for_element(self, element):
        results = [
            self.cottle.relatedness_each(),
            self.cottle.dominance_each(),
        ]

        return list([x[element] for x in results])


class Cottle:
    def __init__(self, stage):
        extractor = ShapeExtractor()
        results = extractor.shapes_for(stage)
        elements = stage.stage_elements()
        tolerance = 0.1

        self.stage = stage
        self.elements = elements

        for e1 in elements:
            results[e1]['dominance'] = 0
            results[e1]['relatedness'] = 0
            p1 = results[e1]['point']
            for e2 in elements:
                if e1 == e2:
                    continue
                p2 = results[e2]['point']

                if p1.area/p2.area > 1 + tolerance:
                    results[e1]['dominance'] += 2

                intersection = p1.intersection(p2)
                if intersection.area == p1.area or intersection.area == p2.area:
                    results[e1]['relatedness'] += 6
                elif intersection.area/p1.area > tolerance:
                    results[e1]['relatedness'] += 4
                elif (p1.distance(p2)**2)/p1.area < tolerance:
                    results[e1]['relatedness'] += 2

        # don't count twice any border
        relatedness = 0
        for i in range(len(elements)):
            e1 = elements[i]
            p1 = results[e1]['point']
            for j in range(i+1, len(elements)):
                e2 = elements[j]
                p2 = results[e2]['point']

                intersection = p1.intersection(p2)
                if intersection.area == p1.area or intersection.area == p2.area:
                    relatedness += 6
                elif intersection.area/p1.area > tolerance:
                    relatedness += 4
                elif (p1.distance(p2)**2)/p1.area < tolerance:
                    relatedness += 2
        self._relatedness = relatedness

        self.results = results

    def relatedness_each(self):
        # atomistic, contiguous, integrated_projected
        return valmap(lambda x: x['relatedness'], self.results)

    def dominance_each(self):
        # 0 - abscence, 2 - secondary, 4 - dominance
        return valmap(lambda x: x['dominance'], self.results)

    def relatedness_all(self):
        return self._relatedness

    def dominance_all(self):
        return sum(self.dominance_each().values())

    def relatedness_group(self):
        value = self.relatedness_all()

        if value < 2 * (len(self.elements) - 1):
            return "atomistic"
        elif value < 4 * (len(self.elements) - 1):
            return "contiguous"
        else:
            return "integrated_projected"

    def dominance_group(self):
        value = self.dominance_all()

        if value == 0:
            return "absence"
        elif value < len(self.elements) * (len(self.elements)-1):
            return "secondary"
        else:
            return "dominance"


class ShapeExtractor:
    def shapes_for(self, stage):
        self.elements = stage.stage_elements()
        return stage.visit(self)

    def case_present_past_future(self, stage):
        results = {}
        for e in self.elements:
            data = stage.element_data(e)
            p = Point(data['center_x'], 500 - data['center_y'])
            results[e] = {
                'point': p.buffer(data['radius'])
            }
        return results

    def case_seasons_of_year(self, stage):
        results = {}
        for e in self.elements:
            data = stage.element_data(e)
            results[e] = {
                'point': box(
                    data['center_x'] - data['size_x']/2,
                    500 - data['center_y'] - data['size_y']/2,
                    data['center_x'] + data['size_x']/2,
                    500 - data['center_y'] + data['size_y']/2)
            }
        return results

    def case_days_of_week(self, stage):
        results = {}
        for e in self.elements:
            data = stage.element_data(e)
            results[e] = {
                'point': box(
                    data['center_x'] - 50/2,
                    500 - data['center_y'] - data['size_y']/2,
                    data['center_x'] + 50/2,
                    500 - data['center_y'] + data['size_y']/2)
            }
        return results

    def case_parts_of_day(self, stage):
        results = {}
        for e in self.elements:
            data = stage.element_data(e)
            results[e] = {
                'point': CircularAdapter(data['rotation'], data['size'], 200)
            }
        return results

    @staticmethod
    def intersection(one, two):
        return one.intersection(two).area

    @staticmethod
    def distance(one, two):
        return one.distance(two)


class CircularAdapter:
    def __init__(self, rotation, size, radius):
        self._rotation = rotation
        self._size = size
        self._radius = radius

        points = [(0, 0)]
        count = max(2, math.ceil(self._size * 16 / 360))
        angle = math.radians(self._rotation - self._size/2)
        size = math.radians(self._size)
        for i in range(count+1):
            x = math.cos(angle + i/count * size) * self._radius
            y = math.sin(angle + i/count * size) * self._radius
            points.append((x, y))

        self._shape = Polygon(points)

    @property
    def area(self):
        return self._shape.area

    def intersection(self, other):
        result = self._shape.intersection(other._shape)
        return CircularWrapper(result)

    def union(self, other):
        result = self._shape.union(other._shape)
        return CircularWrapper(result)

    def distance(self, other):
        dist_a = (self._rotation - other._rotation) % 360
        dist_b = (other._rotation - self._rotation) % 360
        dist = min(dist_a, dist_b) - (self._size + other._size) / 2
        return max(0, dist)


class CircularWrapper:
    def __init__(self, shape):
        self._shape = shape

    @property
    def area(self):
        return self._shape.area

    def intersection(self, other):
        result = self._shape.intersection(other._shape)
        return CircularWrapper(result)

    def union(self, other):
        result = self._shape.union(other._shape)
        return CircularWrapper(result)
