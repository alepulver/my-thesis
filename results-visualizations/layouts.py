import pyx
import math


def all_layouts():
    return [CircularLayout, RectangularLayout]


def available_names():
    return [e.name for e in all_layouts()]


def from_name(name):
    mapping = {e.name: e for e in all_layouts()}
    return mapping[name]


class Layout:
    def draw(self, sampler, canvas):
        raise NotImplementedError()


class CircularLayout(Layout):
    name = 'circular'

    def draw(self, sampler, canvas):
        pass


class RectangularLayout(Layout):
    name = 'rectangular'

    def __init__(self):
        self.width = 10

    @staticmethod
    def item_size_for(width, height, n):
        area = width*height / n
        side = math.sqrt(area)

        per_column = max(1, math.floor(height/side))
        per_row = n / per_column

        if per_row*side > width:
            side -= (math.ceil(per_row)*side - width) / math.ceil(per_row)
        return side

    def draw(self, sampler, canvas):
        clusters = {name: sampler.sample(name) for name in sampler.cluster_names()}
        total_items = sum(len(x) for x in clusters.values())
        item_size = min(self.item_size_for(1, len(x)/total_items, len(x)) for x in clusters.values())

        margin = 0.1 * item_size
        item_size -= margin

        start_y = 0
        for k, v in clusters.items():
            start_y += margin
            height = (len(v)/total_items)
            line = pyx.path.line(0, start_y + height, 1, start_y + height)
            canvas.stroke(line, [pyx.style.linewidth(0.001)])

            index = 0
            for element in v:
                per_column = max(1, math.floor(height / (item_size+margin)))
                row = index % per_column
                column = index // per_column


                figure = pyx.canvas.canvas()
                element['stage'].draw(figure)
                transform = pyx.trafo.scale(item_size * 1/800, item_size * 1/800)
                transform = transform.translated(column * (item_size+margin), start_y + row*(item_size+margin))
                canvas.insert(figure, [transform])

                index += 1

            start_y += height + 2*margin