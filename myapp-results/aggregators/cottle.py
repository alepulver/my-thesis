from shapely.geometry import Point
from toolz.dicttoolz import valmap


class Cottle:
    def __init__(self, stage):
        self.stage = stage
        elements = stage.stage_elements()
        data = stage._data['results']['drawing']['shapes']
        results = {}
        for e in elements:
            v = data[e]
            results[e] = {
                'point': Point(v['position']['x'], v['position']['y']).buffer(v['radius'])
            }

        for e1 in elements:
            results[e1]['intersection'] = 0
            results[e1]['dominance'] = 0
            p1 = results[e1]['point']
            for e2 in elements:
                if e1 == e2:
                    continue
                p2 = results[e2]['point']
                results[e1]['intersection'] += p1.intersection(p2).area
                if p1.area > p2.area:
                    results[e1]['dominance'] += 2

        self.results = results

    def relatedness(self):
        # atomistic, contiguous, integrated_projected
        return valmap(lambda x: x['intersection'], self.results)

    def dominance(self):
        # 0 - abscence, 2 - secondary, 4 - dominance
        return valmap(lambda x: x['dominance'], self.results)
