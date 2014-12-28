from shapely.geometry import Point
from toolz.dicttoolz import valmap
from shapely.geometry import box


class Cottle:
    def __init__(self, stage):
        extractor = ShapeExtractor()
        results = extractor.shapes_for(stage)
        elements = stage.stage_elements()

        for e1 in elements:
            results[e1]['dominance'] = 0
            results[e1]['relatedness'] = 0
            p1 = results[e1]['point']
            for e2 in elements:
                if e1 == e2:
                    continue
                p2 = results[e2]['point']

                if p1.area > p2.area:
                    results[e1]['dominance'] += 2

                if p1.intersection(p2).area == p1.area or p1.intersection(p2).area == p2.area:
                    results[e1]['relatedness'] += 6
                elif p1.intersection(p2).area > 0:
                    results[e1]['relatedness'] += 4
                elif p1.distance(p2) < 10:
                    results[e1]['relatedness'] += 2

        # don't count twice any border
        relatedness = 0
        for i in range(len(elements)):
            e1 = elements[i]
            p1 = results[e1]['point']
            for j in range(i+1, len(elements)):
                e2 = elements[j]
                p2 = results[e2]['point']

                if p1.intersection(p2).area == p1.area or p1.intersection(p2).area == p2.area:
                    relatedness += 6
                elif p1.intersection(p2).area > 0:
                    relatedness += 4
                elif p1.distance(p2) < 10:
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


# FIXME: don't directly access stage JSON, use element_data
class ShapeExtractor:
    def shapes_for(self, stage):
        self.elements = stage.stage_elements()
        return stage.visit(self)

    def case_present_past_future(self, stage):
        data = stage._data['results']['drawing']['shapes']
        results = {}
        for e in self.elements:
            v = data[e]
            results[e] = {
                'point': Point(v['position']['x'], 500-v['position']['y']).buffer(v['radius'], 64)
            }
        return results

    def case_seasons_of_year(self, stage):
        data = stage._data['results']['drawing']['shapes']
        results = {}
        for e in self.elements:
            v = data[e]
            results[e] = {
                'point': box(v['position']['x'] - v['size']['width']/2, 500-v['position']['y'] - v['size']['height']/2, v['position']['x'] + v['size']['width']/2, 500-v['position']['y'] + v['size']['height']/2)
            }
        return results
