from shapely.geometry import Point
from toolz.dicttoolz import valmap
from shapely.geometry import box


class CottleWrapper:
    def __init__(self, stage):
        self.cottle = Cottle(stage)
        self.cottle_ext = ExtendedCottle(stage)

    def row_for_stage(self):
        return [
            self.cottle.relatedness_all(),
            self.cottle.dominance_all(),
            self.cottle_ext.separation_all(),
            self.cottle_ext.intersection_all(),
            self.cottle_ext.dominance_all(),
            self.cottle_ext.coverage_all()
        ]

    def row_for_element(self, element):
        results = [
            self.cottle.relatedness_each(),
            self.cottle.dominance_each(),
            self.cottle_ext.separation_each(),
            self.cottle_ext.intersection_each(),
            self.cottle_ext.dominance_each(),
            self.cottle_ext.coverage_each()
        ]

        return list([x[element] for x in results])


class Cottle:
    def __init__(self, stage):
        extractor = ShapeExtractor()
        results = extractor.shapes_for(stage)
        elements = stage.stage_elements()
        tolerance = 0.1

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


class ExtendedCottle:
    def __init__(self, stage):
        extractor = ShapeExtractor()
        results = extractor.shapes_for(stage)
        elements = stage.stage_elements()

        for e1 in elements:
            results[e1]['dominance'] = 0
            results[e1]['intersection'] = 0
            results[e1]['separation'] = 0

            p1 = results[e1]['point']
            results[e1]['coverage'] = p1.area / (800 * 500)
            for e2 in elements:
                if e1 == e2:
                    continue
                p2 = results[e2]['point']

                if p1.area/p2.area > 1:
                    results[e1]['dominance'] += p1.area/p2.area

                intersection = p1.intersection(p2)
                results[e1]['intersection'] += intersection.area/p1.area

                if intersection.area == 0:
                    results[e1]['separation'] += (p1.distance(p2)**2)/p1.area

        # don't count twice any border
        relatedness = 0
        separation = 0

        for i in range(len(elements)):
            e1 = elements[i]
            p1 = results[e1]['point']
            for j in range(i+1, len(elements)):
                e2 = elements[j]
                p2 = results[e2]['point']

                intersection = p1.intersection(p2)
                relatedness += intersection.area/p1.area

                if intersection.area == 0:
                    separation += (p1.distance(p2)**2)/p1.area

        coverage = Point(0, 0)
        for e in elements:
            p = results[e]['point']
            coverage = coverage.union(p)

        self._relatedness = relatedness
        self._separation = separation
        self._coverage = coverage.area

        self.results = results

    def intersection_each(self):
        return valmap(lambda x: x['intersection'], self.results)

    def separation_each(self):
        return valmap(lambda x: x['separation'], self.results)

    def dominance_each(self):
        return valmap(lambda x: x['dominance'], self.results)

    def coverage_each(self):
        return valmap(lambda x: x['coverage'], self.results)

    def intersection_all(self):
        return self._relatedness

    def separation_all(self):
        return self._separation

    def dominance_all(self):
        return sum(self.dominance_each().values())

    def coverage_all(self):
        return self._coverage


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

    @staticmethod
    def intersection(one, two):
        return one.intersection(two).area

    @staticmethod
    def distance(one, two):
        return one.distance(two)
